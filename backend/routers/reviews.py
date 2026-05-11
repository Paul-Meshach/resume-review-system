import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.review import Review, ReviewStatus
from models.candidate import Candidate
from models.user import User, UserRole
from models.notification import Notification
from schemas.review import SendReviewRequest, SubmitReviewRequest, ReviewResponse
from services.auth_service import require_admin
from services.email_service import send_review_request_email, send_admin_notification_email

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/send")
def send_for_review(
        payload: SendReviewRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_admin)
):
    """
    Admin sends resume to a TL for review
    1. Validate candidate and TL exist
    2. Generate unique review token (magic link)
    3. Create review record in DB
    4. Send email to TL
    """
    candidate = db.query(Candidate).filter(Candidate.id == payload.candidate_id).first()
    if not candidate:
        raise HTTPException(404, detail="Candidate not found")

    tl = db.query(User).filter(
        User.id == payload.tl_id,
        User.role == UserRole.tl
    ).first()
    if not tl:
        raise HTTPException(404, detail="Team Lead not found")

    # Check if already sent to this TL
    existing = db.query(Review).filter(
        Review.candidate_id == candidate.id,
        Review.assigned_tl_id == tl.id,
        Review.status == ReviewStatus.pending
    ).first()
    if existing:
        raise HTTPException(400, detail="Resume already sent to this TL and is pending review")

    # Generate a cryptographically random token (not guessable)
    review_token = str(uuid.uuid4())
    token_expiry = datetime.utcnow() + timedelta(hours=72)

    review = Review(
        candidate_id=candidate.id,
        assigned_tl_id=tl.id,
        review_token=review_token,
        token_expiry=token_expiry,
        status=ReviewStatus.pending
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    # Send email — wrap in try/except so DB record isn't rolled back if email fails
    try:
        send_review_request_email(
            tl_email=tl.email,
            tl_name=tl.name,
            candidate={
                "name": candidate.name,
                "email": candidate.email,
                "phone": candidate.phone,
                "qualification": candidate.qualification,
                "skills": candidate.skills,
                "years_of_experience": candidate.years_of_experience,
                "domain": candidate.domain,
            },
            review_token=review_token,
            resume_path=candidate.resume_file_path
        )
    except Exception as e:
        # Log error but don't fail the request — email can be retried
        print(f"Email send failed: {e}")
        return {"message": "Review assigned but email sending failed", "review_id": review.id}

    return {"message": "Resume sent for review successfully", "review_id": review.id}


@router.get("/by-token/{token}")
def get_review_by_token(token: str, db: Session = Depends(get_db)):
    """
    TL uses this to get review details from their email link
    No authentication needed — token IS the authentication
    """
    review = db.query(Review).filter(Review.review_token == token).first()
    if not review:
        raise HTTPException(404, detail="Invalid review link")
    if review.token_expiry and datetime.utcnow() > review.token_expiry:
        raise HTTPException(410, detail="Review link has expired")
    if review.status != ReviewStatus.pending:
        raise HTTPException(400, detail="This resume has already been reviewed")

    candidate = review.candidate
    tl = review.assigned_tl

    return {
        "review_id": review.id,
        "candidate": {
            "name": candidate.name,
            "email": candidate.email,
            "phone": candidate.phone,
            "qualification": candidate.qualification,
            "skills": candidate.skills,
            "years_of_experience": candidate.years_of_experience,
            "domain": candidate.domain,
        },
        "tl_name": tl.name,
        "assigned_at": review.assigned_at,
    }


@router.post("/submit")
def submit_review(payload: SubmitReviewRequest, db: Session = Depends(get_db)):
    """
    TL submits their decision — shortlisted or rejected
    No JWT auth — token from email is used instead
    """
    review = db.query(Review).filter(Review.review_token == payload.token).first()
    if not review:
        raise HTTPException(404, detail="Invalid token")
    if review.token_expiry and datetime.utcnow() > review.token_expiry:
        raise HTTPException(410, detail="Review link expired")
    if review.status != ReviewStatus.pending:
        raise HTTPException(400, detail="Already reviewed")

    # Update review
    review.status = payload.status
    review.comments = payload.comments
    review.reviewed_at = datetime.utcnow()

    # Find the admin who uploaded this candidate
    candidate = review.candidate
    admin = db.query(User).filter(
        User.id == candidate.uploaded_by,
        User.role == UserRole.admin
    ).first()

    if admin:
        # Create in-app notification
        message = (
            f"Candidate '{candidate.name}' was "
            f"{'✅ Shortlisted' if payload.status == 'shortlisted' else '❌ Rejected'} "
            f"by {review.assigned_tl.name}."
        )
        notification = Notification(
            admin_id=admin.id,
            review_id=review.id,
            message=message
        )
        db.add(notification)

        # Send email to admin too
        try:
            send_admin_notification_email(
                admin_email=admin.email,
                admin_name=admin.name,
                candidate_name=candidate.name,
                tl_name=review.assigned_tl.name,
                status=payload.status.value,
                comments=payload.comments
            )
        except Exception as e:
            print(f"Admin email notification failed: {e}")

    db.commit()
    return {"message": "Review submitted successfully", "status": payload.status}
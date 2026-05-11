import os, uuid, shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.candidate import Candidate
from models.user import User
from schemas.candidate import CandidateResponse
from services.auth_service import require_admin
from services.parser import parse_resume
from fastapi.responses import FileResponse

router = APIRouter(prefix="/resumes", tags=["Resumes"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx"}


@router.post("/upload", response_model=CandidateResponse)
async def upload_resume(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(require_admin)
):
    """
    Upload resume file + auto-parse it
    Steps:
    1. Validate file type
    2. Save file to disk with unique name
    3. Parse the file
    4. Save extracted data to DB
    5. Return extracted data
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, detail=f"Only PDF, DOC, DOCX allowed. Got: {ext}")

    # Generate unique filename to prevent overwrites and path traversal attacks
    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse resume
    try:
        extracted = parse_resume(file_path)
    except Exception as e:
        os.remove(file_path)  # Clean up file if parsing fails
        raise HTTPException(422, detail=f"Could not parse resume: {str(e)}")

    # Save to database
    candidate = Candidate(
        **extracted,
        resume_file_path=file_path,
        original_filename=file.filename,
        uploaded_by=current_user.id
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


@router.get("/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
        candidate_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_admin)
):
    """Get a specific candidate's extracted data"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(404, detail="Candidate not found")
    return candidate


@router.get("/{candidate_id}/download")
def download_resume(
        candidate_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_admin)
):
    """Download original resume file"""
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if not candidate:
        raise HTTPException(404, detail="Candidate not found")
    if not os.path.exists(candidate.resume_file_path):
        raise HTTPException(404, detail="Resume file not found on server")

    return FileResponse(
        candidate.resume_file_path,
        filename=candidate.original_filename,
        media_type="application/octet-stream"
    )
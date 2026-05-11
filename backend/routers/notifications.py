from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.notification import Notification
from models.user import User
from schemas.review import NotificationResponse
from services.auth_service import require_admin
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Get all notifications for the logged-in admin"""
    return db.query(Notification).filter(
        Notification.admin_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()

@router.patch("/{notification_id}/read")
def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Mark a notification as read"""
    notif = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.admin_id == current_user.id
    ).first()
    if notif:
        notif.is_read = True
        db.commit()
    return {"message": "Marked as read"}

@router.get("/unread-count")
def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    count = db.query(Notification).filter(
        Notification.admin_id == current_user.id,
        Notification.is_read == False
    ).count()
    return {"count": count}
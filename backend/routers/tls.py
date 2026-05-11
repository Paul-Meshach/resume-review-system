from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from schemas.auth import UserResponse
from services.auth_service import require_admin
from typing import List

router = APIRouter(prefix="/tls", tags=["Team Leads"])

@router.get("/", response_model=List[UserResponse])
def list_tls(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Return all Team Lead users — for TL selection screen"""
    tls = db.query(User).filter(
        User.role == UserRole.tl,
        User.is_active == True
    ).all()
    return tls
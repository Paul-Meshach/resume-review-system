# routers/auth.py — UPDATED with UPSERT logic + password reset endpoint

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from schemas.auth import LoginRequest, TokenResponse, UserResponse
from services.auth_service import (
    hash_password, verify_password,
    create_access_token, get_current_user
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role.value,
        "name": user.name
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role.value,
        "name": user.name,
        "user_id": user.id
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# ─────────────────────────────────────────────
# SEED USERS — NOW USES UPSERT (UPDATE OR INSERT)
# ─────────────────────────────────────────────

@router.post("/seed-users")
def seed_users(db: Session = Depends(get_db)):
    """
    FIXED: Now does UPSERT instead of skip-if-exists.
    If a user with that name/role already exists → UPDATE their email + password.
    If they don't exist → INSERT new record.
    Run this every time you change emails in this list.
    """

    # ──────────────────────────────────────────
    # PUT YOUR REAL GMAIL ADDRESSES HERE
    # ──────────────────────────────────────────
    users_to_upsert = [
        {
            "name":     "Admin User",
            "email":    "paulowebmeshach@gmail.com",   # ← CHANGE THIS
            "password": "admin123",
            "role":     UserRole.admin
        },
        {
            "name":     "Alice TL",
            "email":    "pickypercy2000@psnacet.edu.in",     # ← CHANGE THIS
            "password": "tl123",
            "role":     UserRole.tl
        },
        {
            "name":     "Bob TL",
            "email":    "gracejesus2021@gmail.com",     # ← CHANGE THIS
            "password": "tl123",
            "role":     UserRole.tl
        },
        {
            "name":     "Carol TL",
            "email":    "edusolofficekvm@gmail.com",     # ← CHANGE THIS
            "password": "tl123",
            "role":     UserRole.tl
        },
    ]

    results = {"updated": [], "created": []}

    for u in users_to_upsert:
        # Try to find by name (stable identifier even if email changed)
        existing = db.query(User).filter(User.name == u["name"]).first()

        if existing:
            # UPDATE: overwrite email and rehash password
            existing.email         = u["email"]
            existing.password_hash = hash_password(u["password"])
            existing.role          = u["role"]
            existing.is_active     = True
            results["updated"].append(u["email"])
        else:
            # INSERT: brand new user
            new_user = User(
                name          = u["name"],
                email         = u["email"],
                password_hash = hash_password(u["password"]),
                role          = u["role"]
            )
            db.add(new_user)
            results["created"].append(u["email"])

    db.commit()

    return {
        "message": "Seed complete",
        "updated": results["updated"],
        "created": results["created"]
    }


# ─────────────────────────────────────────────
# RESET A SPECIFIC USER'S PASSWORD (utility)
# ─────────────────────────────────────────────

@router.post("/reset-password")
def reset_password(
    email: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    Utility endpoint to fix password for any user by email.
    Use this from Swagger UI → /docs
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(404, detail=f"No user found with email: {email}")

    user.password_hash = hash_password(new_password)
    db.commit()

    return {"message": f"Password reset for {email}"}


# ─────────────────────────────────────────────
# LIST ALL USERS (for verification only)
# ─────────────────────────────────────────────

@router.get("/users-list")
def list_all_users(db: Session = Depends(get_db)):
    """
    Shows all users currently in DB.
    Confirms emails are updated correctly after seed.
    """
    users = db.query(User).all()
    return [
        {
            "id":    u.id,
            "name":  u.name,
            "email": u.email,
            "role":  u.role.value,
            "active": u.is_active
        }
        for u in users
    ]
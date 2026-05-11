# WHY: Users table stores both Admins and Team Leads
# CONCEPT: We use a 'role' column to differentiate — one table, two user types
# This is called Single Table Inheritance — simpler for this project size

from sqlalchemy import Column, Integer, String, Enum, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    tl = "tl"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    # NEVER store plain passwords — always store hashed versions
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.tl)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships — SQLAlchemy auto-joins these for you
    # back_populates creates bidirectional links between tables
    uploaded_resumes = relationship("Candidate", back_populates="uploader")
    assigned_reviews = relationship("Review", back_populates="assigned_tl",
                                    foreign_keys="Review.assigned_tl_id")
    notifications = relationship("Notification", back_populates="admin")
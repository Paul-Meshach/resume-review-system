# WHY: Tracks the entire review workflow
# CONCEPT: review_token is a unique UUID sent in the TL email link
# When TL clicks the link, we verify the token — no login needed for TL review
# This is called "Magic Link" authentication — secure and user-friendly

from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum


class ReviewStatus(str, enum.Enum):
    pending = "pending"
    shortlisted = "shortlisted"
    rejected = "rejected"


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    assigned_tl_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    status = Column(Enum(ReviewStatus), default=ReviewStatus.pending)

    # Magic link token — TL gets this in email, uses it to access review page
    review_token = Column(String(255), unique=True, nullable=False)
    token_expiry = Column(DateTime)  # Tokens expire after 72 hours

    comments = Column(Text)  # Optional TL comments

    assigned_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)  # Set when TL submits decision

    # Relationships
    candidate = relationship("Candidate", back_populates="reviews")
    assigned_tl = relationship("User", back_populates="assigned_reviews",
                               foreign_keys=[assigned_tl_id])
    notification = relationship("Notification", back_populates="review", uselist=False)
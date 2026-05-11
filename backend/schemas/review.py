from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class ReviewStatus(str, Enum):
    pending = "pending"
    shortlisted = "shortlisted"
    rejected = "rejected"

class SendReviewRequest(BaseModel):
    candidate_id: int
    tl_id: int

class SubmitReviewRequest(BaseModel):
    token: str
    status: ReviewStatus
    comments: Optional[str] = None

class ReviewResponse(BaseModel):
    id: int
    status: ReviewStatus
    assigned_at: datetime
    reviewed_at: Optional[datetime]
    comments: Optional[str]

    class Config:
        from_attributes = True

class NotificationResponse(BaseModel):
    id: int
    message: str
    is_read: bool
    created_at: datetime
    review_id: int

    class Config:
        from_attributes = True
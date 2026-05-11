from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CandidateResponse(BaseModel):
    id: int
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    qualification: Optional[str]
    skills: Optional[str]
    years_of_experience: Optional[str]
    domain: Optional[str]
    original_filename: Optional[str]
    uploaded_at: datetime

    class Config:
        from_attributes = True
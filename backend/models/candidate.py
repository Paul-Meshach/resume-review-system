# WHY: Stores all extracted resume data
# CONCEPT: Foreign key to users — every candidate was uploaded by someone (admin)
# resume_file_path stores WHERE the file is on disk, not the file itself (never store files in DB)

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    # Extracted resume fields
    name = Column(String(150))
    email = Column(String(150))
    phone = Column(String(20))
    qualification = Column(String(255))
    skills = Column(Text)  # Stored as comma-separated string
    years_of_experience = Column(String(50))
    domain = Column(String(150))

    # File info
    resume_file_path = Column(String(500), nullable=False)
    original_filename = Column(String(255))

    # Timestamps and foreign key
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(Integer, ForeignKey("users.id"))

    # Relationships
    uploader = relationship("User", back_populates="uploaded_resumes")
    reviews = relationship("Review", back_populates="candidate")
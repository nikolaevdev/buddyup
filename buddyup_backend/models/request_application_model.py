from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class RequestApplication(Base):
    __tablename__ = "request_applications"

    id = Column(Integer, primary_key=True, index=True)
    study_request_id = Column(Integer, ForeignKey("study_requests.id"), nullable=False)
    helper_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, approved, rejected, confirmed, declined
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    study_request = relationship("StudyRequest", back_populates="applications", lazy="selectin")
    helper = relationship("User", lazy="selectin")

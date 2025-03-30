from sqlalchemy import Column, Integer, DateTime, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    study_request_id = Column(Integer, ForeignKey("study_requests.id"), nullable=False)
    meeting_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    location = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    # Eager загрузка отношения к запросу
    study_request = relationship(
        "StudyRequest",
        back_populates="meeting",
        foreign_keys=[study_request_id],
        lazy="selectin"
    )

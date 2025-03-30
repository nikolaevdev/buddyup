# buddyup/models/response_model.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)
    study_request_id = Column(Integer, ForeignKey("study_requests.id"), nullable=False)
    responder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    response_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

    # Связь с запросом
    study_request = relationship("StudyRequest", back_populates="responses", lazy="selectin")
    # Связь с пользователем, который откликнулся
    responder = relationship("User", lazy="selectin")

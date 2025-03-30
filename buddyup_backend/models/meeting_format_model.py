# buddyup/models/meeting_format_model.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class MeetingFormat(Base):
    __tablename__ = "meeting_formats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


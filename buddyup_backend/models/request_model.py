# buddyup/models/request_model.py
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String, Boolean, Table
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime, timezone
from models.meeting_format_model import MeetingFormat
from models.subject_model import Subject

# Ассоциация для предметов, по которым требуется помощь в запросе
request_subject_association = Table(
    "request_subject_association",
    Base.metadata,
    Column("request_id", Integer, ForeignKey("study_requests.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)

class StudyRequest(Base):
    __tablename__ = "study_requests"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(Text, nullable=False)
    task_description = Column(Text, nullable=False)

    meeting_format_id = Column(Integer, ForeignKey("meeting_formats.id"), nullable=False)
    # Добавляем eager загрузку для meeting_format
    meeting_format = relationship("MeetingFormat", lazy="selectin")

    preferred_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    location = Column(String, nullable=True)
    additional_notes = Column(Text, nullable=True)

    course = Column(Integer, nullable=False)  # Курс (1-6)
    study_type = Column(String, nullable=False)  # Тип обучения (бакалавриат, магистратура, аспирантура)

    is_confirmed = Column(Boolean, default=False)

    # Отношение к встрече – используем eager загрузку
    meeting = relationship(
        "Meeting",
        back_populates="study_request",
        uselist=False,
        primaryjoin="StudyRequest.id==Meeting.study_request_id",
        lazy="selectin"
    )

    creator_id = Column(Integer, ForeignKey("users.id"))
    # Eager загрузка для создателя запроса
    creator = relationship("User", back_populates="study_requests", lazy="selectin")

    subjects = relationship("Subject", secondary=request_subject_association, backref="study_requests", lazy="selectin")

    responses = relationship("Response", back_populates="study_request", cascade="all, delete-orphan", lazy="selectin")

    applications = relationship("RequestApplication", back_populates="study_request", cascade="all, delete-orphan", lazy="selectin")

# buddyup/models/user_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base import Base
from models.subject_model import Subject
from models.meeting_format_model import MeetingFormat

# Ассоциационные таблицы
user_subject_need = Table(
    "user_subject_need",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)

user_subject_can_help = Table(
    "user_subject_can_help",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True)
    fio = Column(String)
    group_number = Column(String)
    course = Column(String, nullable=True)

    # Загружаем связанные объекты жадно (selectin)
    subjects_need_help = relationship(
        "Subject", secondary=user_subject_need, backref="users_need", lazy="selectin"
    )
    subjects_can_help = relationship(
        "Subject", secondary=user_subject_can_help, backref="users_can_help", lazy="selectin"
    )

    preferred_meeting_format_id = Column(Integer, ForeignKey("meeting_formats.id"), nullable=True)
    preferred_meeting_format = relationship("MeetingFormat", lazy="selectin")

    study_requests = relationship("StudyRequest", back_populates="creator", lazy="selectin")

    feedback_authored = relationship(
        "Feedback", foreign_keys="Feedback.author_id", back_populates="author", lazy="selectin"
    )
    feedback_received = relationship(
        "Feedback", foreign_keys="Feedback.target_user_id", back_populates="target_user", lazy="selectin"
    )





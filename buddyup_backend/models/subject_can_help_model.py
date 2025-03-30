# buddyup/models/subject_can_help_model.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from models.base import Base

class SubjectCanHelp(Base):
    __tablename__ = "subjects_can_help"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    __table_args__ = (UniqueConstraint('name', name='uq_subject_can_help_name'),)

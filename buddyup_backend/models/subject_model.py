# buddyup/models/subject_model.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from models.base import Base

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    __table_args__ = (UniqueConstraint('name', name='uq_subject_name'),)




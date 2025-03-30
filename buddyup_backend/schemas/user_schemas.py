# buddyup/schemas/user_schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from schemas.subject_schemas import SubjectRead
from schemas.meeting_format_schemas import MeetingFormatRead

class UserCreate(BaseModel):
    uid: str = Field(..., min_length=1)
    fio: str = Field(..., min_length=1)
    group_number: str = Field(..., min_length=1)
    course: str = Field(default="", description="Курс пользователя")  # Явно строка
    subjects_need_help: List[int] = Field(default_factory=list, description="Список ID предметов, по которым нужна помощь")
    subjects_can_help: List[int] = Field(default_factory=list, description="Список ID предметов, по которым можно помочь")
    preferred_meeting_format_id: Optional[int] = Field(None, description="ID предпочитаемого формата встречи")

    class Config:
        from_attributes = True

class UserRead(BaseModel):
    id: int
    uid: str
    fio: str
    group_number: str
    course: Optional[str] = None
    subjects_need_help: List[SubjectRead] = []
    subjects_can_help: List[SubjectRead] = []
    preferred_meeting_format: Optional[MeetingFormatRead] = None

    class Config:
        from_attributes = True


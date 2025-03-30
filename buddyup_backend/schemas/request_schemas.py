# buddyup/schemas/request_schemas.py
# buddyup/schemas/request_schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict
from datetime import datetime
from schemas.meeting_format_schemas import MeetingFormatRead  # импортируем схему формата встречи
from schemas.response_schemas import ResponseRead

class StudyRequestCreate(BaseModel):
    subject: str = Field(..., min_length=1)
    task_description: str = Field(..., min_length=1)
    meeting_format_id: int
    preferred_time: Optional[datetime] = None
    location: Optional[str] = Field(None, description="Локация встречи")
    additional_notes: Optional[str] = Field(None, description="Дополнительная информация")
    course: int = Field(..., ge=1, le=6, description="Курс обучения")
    study_type: str = Field(..., description="Тип обучения: бакалавриат, магистратура, аспирантура")
    subjects: List[int] = Field(..., description="Список ID предметов, по которым нужна помощь")

    class Config:
        from_attributes = True

class StudyRequestUpdate(BaseModel):
    subject: Optional[str] = None
    task_description: Optional[str] = None
    meeting_format_id: Optional[int] = None
    preferred_time: Optional[datetime] = None
    location: Optional[str] = None
    additional_notes: Optional[str] = None
    course: Optional[int] = None
    study_type: Optional[str] = None
    subjects: Optional[List[int]] = None

    class Config:
        from_attributes = True

class StudyRequestRead(BaseModel):
    id: int
    creator_uid: int  # новое поле для uid пользователя
    subject: str
    task_description: str
    meeting_format_id: int
    # Новый вложенный объект с информацией о формате встречи
    meeting_format_info: MeetingFormatRead
    subjects_info: List[Dict[str, Any]]  # новое поле, содержащее id и название предмета
    preferred_time: Optional[datetime]
    location: Optional[str] = None
    additional_notes: Optional[str] = None
    course: int
    study_type: str
    is_confirmed: bool
    creator_id: int
    subjects: List[int] = []      # Список ID предметов
    responses: List[int] = []     # Список ID пользователей, откликнувшихся
    applications: List[int] = []  # Список ID заявок

    class Config:
        from_attributes = True



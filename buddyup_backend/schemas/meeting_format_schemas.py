# buddyup/schemas/meeting_format_schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class MeetingFormatCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, description="Описание формата встречи")

    class Config:
        from_attributes = True

class MeetingFormatRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

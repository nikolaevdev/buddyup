from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MeetingCreate(BaseModel):
    study_request_id: int
    meeting_time: datetime
    location: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class MeetingRead(BaseModel):
    id: int
    study_request_id: int
    meeting_time: datetime
    location: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

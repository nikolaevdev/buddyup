# buddyup/schemas/subject_need_schemas.py
from pydantic import BaseModel, Field

class SubjectNeedCreate(BaseModel):
    name: str = Field(..., min_length=1)

class SubjectNeedRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

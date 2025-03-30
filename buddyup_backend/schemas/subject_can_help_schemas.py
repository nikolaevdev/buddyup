# buddyup/schemas/subject_can_help_schemas.py
from pydantic import BaseModel, Field

class SubjectCanHelpCreate(BaseModel):
    name: str = Field(..., min_length=1)

class SubjectCanHelpRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

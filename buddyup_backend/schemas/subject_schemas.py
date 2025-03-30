from pydantic import BaseModel, Field

class SubjectCreate(BaseModel):
    name: str = Field(..., min_length=1)

class SubjectRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field
from datetime import datetime

class RequestApplicationRead(BaseModel):
    id: int
    study_request_id: int
    helper_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class RequestApplicationUpdate(BaseModel):
    status: str = Field(..., description="Новый статус: approved, rejected, confirmed, declined")

    class Config:
        from_attributes = True

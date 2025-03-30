# buddyup/schemas/response_schemas.py
from pydantic import BaseModel
from datetime import datetime

class ResponseRead(BaseModel):
    id: int
    study_request_id: int
    responder_id: int
    response_time: datetime

    class Config:
        from_attributes = True

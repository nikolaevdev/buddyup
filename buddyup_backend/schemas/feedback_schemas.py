# buddyup/schemas/feedback_schemas.py

from pydantic import BaseModel, Field
from typing import Optional
from utils.sanitizer import sanitize_field

class FeedbackCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.comment:
            self.comment = sanitize_field(self.comment)

class FeedbackRead(BaseModel):
    id: int
    rating: int
    comment: Optional[str]
    author_id: int
    target_user_id: int

    class Config:
        from_attributes = True

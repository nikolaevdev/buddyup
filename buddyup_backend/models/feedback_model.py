# buddyup/models/feedback_model.py

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    comment = Column(Text, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"))
    target_user_id = Column(Integer, ForeignKey("users.id"))

    # Eager загрузка для автора отзыва
    author = relationship(
        "User",
        foreign_keys=[author_id],
        back_populates="feedback_authored",
        lazy="selectin"
    )
    # Eager загрузка для пользователя, которому оставлен отзыв
    target_user = relationship(
        "User",
        foreign_keys=[target_user_id],
        back_populates="feedback_received",
        lazy="selectin"
    )

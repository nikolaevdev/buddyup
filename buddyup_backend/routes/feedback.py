from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_cache.decorator import cache

from models.db import get_db
from models.user_model import User
from models.feedback_model import Feedback
from schemas.feedback_schemas import FeedbackCreate, FeedbackRead
from logs.logger_config import logger
from schemas.standard_response import StandardResponse

router = APIRouter()

@router.post("/{target_uid}", response_model=StandardResponse[FeedbackRead])
async def leave_feedback(
        target_uid: str,
        feedback: FeedbackCreate,
        fio: str = Query(..., description="ФИО отправителя"),
        gn: str = Query(..., description="Номер группы отправителя"),
        uid: str = Query(..., description="Уникальный идентификатор отправителя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Создает отзыв для пользователя с указанным target_uid.
    """
    logger.info(f"[POST /feedback/{target_uid}] Отзыв от uid={uid}")
    author = await _get_or_create_user(uid, fio, gn, db)
    target_user = await db.scalar(select(User).where(User.uid == target_uid))
    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь (target_uid) не найден")

    if author.id == target_user.id:
        raise HTTPException(status_code=400, detail="Нельзя оставить отзыв самому себе")

    new_fb = Feedback(
        author_id=author.id,
        target_user_id=target_user.id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    db.add(new_fb)
    await db.commit()
    await db.refresh(new_fb)
    logger.info(f"Добавлен отзыв id={new_fb.id} от uid={author.uid} к uid={target_user.uid}")
    return StandardResponse[FeedbackRead](
        status="success",
        message="Отзыв успешно создан",
        id=new_fb.id,
        data=_convert_feedback_to_read(new_fb)
    )

@router.get("/by-user/{user_uid}", response_model=StandardResponse[List[FeedbackRead]])
@cache(expire=60)
async def get_feedback_for_user(
        user_uid: str,
        fio: str = Query(..., description="ФИО запрашивающего пользователя"),
        gn: str = Query(..., description="Номер группы запрашивающего пользователя"),
        uid: str = Query(..., description="UID запрашивающего пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает все отзывы для пользователя с указанным UID.
    """
    logger.info(f"[GET /feedback/by-user/{user_uid}] Запрос отзывов")
    user = await db.scalar(select(User).where(User.uid == user_uid))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    result = await db.execute(select(Feedback).where(Feedback.target_user_id == user.id))
    feedbacks = result.scalars().all()
    if not feedbacks:
        return StandardResponse[List[FeedbackRead]](
            status="success",
            message="Отзывы не найдены",
            data=[]
        )
    return StandardResponse[List[FeedbackRead]](
        status="success",
        message="Отзывы успешно получены",
        data=[_convert_feedback_to_read(fb) for fb in feedbacks]
    )

def _convert_feedback_to_read(fb: Feedback) -> FeedbackRead:
    return FeedbackRead(
        id=fb.id,
        rating=fb.rating,
        comment=fb.comment,
        author_id=fb.author_id,
        target_user_id=fb.target_user_id
    )

async def _get_or_create_user(uid: str, fio: str, gn: str, db: AsyncSession) -> User:
    user = await db.scalar(select(User).where(User.uid == uid))
    if not user:
        user = User(uid=uid, fio=fio, group_number=gn)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Создан пользователь uid={uid}")
    return user

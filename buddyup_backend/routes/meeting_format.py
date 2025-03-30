# buddyup/routes/meeting_format.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi_cache.decorator import cache

from models.db import get_db
from models.meeting_format_model import MeetingFormat
from schemas.meeting_format_schemas import MeetingFormatCreate, MeetingFormatRead
from logs.logger_config import logger
from schemas.standard_response import StandardResponse

router = APIRouter()

@router.post("/", response_model=StandardResponse[MeetingFormatRead])
async def create_meeting_format(
        data: MeetingFormatCreate,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Создает новый формат встречи.
    """
    logger.info(f"[POST /meeting-format] Создание формата: {data.name} от uid={uid}")
    existing = await db.scalar(select(MeetingFormat).where(MeetingFormat.name == data.name))
    if existing:
        raise HTTPException(status_code=400, detail="Такой формат уже существует")
    mf = MeetingFormat(name=data.name, description=data.description)
    db.add(mf)
    await db.commit()
    await db.refresh(mf)
    logger.info(f"Создан meeting_format с id={mf.id}")
    return StandardResponse[MeetingFormatRead](
        status="success",
        message="Формат встречи успешно создан",
        id=mf.id,
        data=mf
    )

@router.get("/", response_model=StandardResponse[List[MeetingFormatRead]])
@cache(expire=60)
async def list_meeting_formats(
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает список всех форматов встреч.
    """
    logger.info(f"[GET /meeting-format] Запрос списка форматов от uid={uid}")
    result = await db.execute(select(MeetingFormat))
    formats = result.scalars().all()
    if not formats:
        return StandardResponse[List[MeetingFormatRead]](
            status="success",
            message="Форматы не найдены",
            data=[]
        )
    return StandardResponse[List[MeetingFormatRead]](
        status="success",
        message="Форматы успешно получены",
        data=formats
    )

@router.get("/{format_id}", response_model=StandardResponse[MeetingFormatRead])
async def get_one_format(
        format_id: int,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает формат встречи по его ID.
    """
    logger.info(f"[GET /meeting-format/{format_id}] Запрос формата от uid={uid}")
    mf = await db.get(MeetingFormat, format_id)
    if not mf:
        raise HTTPException(status_code=404, detail="Формат не найден")
    return StandardResponse[MeetingFormatRead](
        status="success",
        message="Формат успешно получен",
        id=mf.id,
        data=mf
    )

@router.put("/{format_id}", response_model=StandardResponse[MeetingFormatRead])
async def update_format(
        format_id: int,
        data: MeetingFormatCreate,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Обновляет формат встречи по его ID.
    """
    logger.info(f"[PUT /meeting-format/{format_id}] Обновление формата от uid={uid}")
    mf = await db.get(MeetingFormat, format_id)
    if not mf:
        raise HTTPException(status_code=404, detail="Формат не найден")
    existing = await db.scalar(
        select(MeetingFormat).where(MeetingFormat.name == data.name, MeetingFormat.id != format_id)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Такое название уже используется")
    mf.name = data.name
    mf.description = data.description
    db.add(mf)
    await db.commit()
    await db.refresh(mf)
    logger.info(f"Обновлён meeting_format id={mf.id} -> name={mf.name}")
    return StandardResponse[MeetingFormatRead](
        status="success",
        message="Формат встречи успешно обновлен",
        id=mf.id,
        data=mf
    )

@router.delete("/{format_id}", response_model=StandardResponse[dict])
async def delete_format(
        format_id: int,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Удаляет формат встречи по его ID.
    """
    logger.info(f"[DELETE /meeting-format/{format_id}] Запрос удаления от uid={uid}")
    mf = await db.get(MeetingFormat, format_id)
    if not mf:
        raise HTTPException(status_code=404, detail="Формат не найден")
    await db.delete(mf)
    await db.commit()
    logger.info(f"Удалён meeting_format id={format_id}")
    return StandardResponse[dict](
        status="success",
        message="Формат успешно удалён",
        id=format_id,
        data={"deleted": True}
    )

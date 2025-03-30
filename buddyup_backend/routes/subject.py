from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from fastapi_cache.decorator import cache

from models.db import get_db
from models.subject_model import Subject
from schemas.subject_schemas import SubjectCreate, SubjectRead
from logs.logger_config import logger
from schemas.standard_response import StandardResponse

router = APIRouter()

@router.post("/", response_model=StandardResponse[SubjectRead])
async def create_subject(
        data: SubjectCreate,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Создает новый предмет, если его нет. Если предмет уже существует, возвращается существующая запись.
    """
    logger.info(f"[POST /subject] Создание предмета: {data.name} от uid={uid}")
    existing = await db.scalar(select(Subject).where(Subject.name == data.name))
    if existing:
        return StandardResponse[SubjectRead](
            status="success",
            message="Предмет уже существует, возвращаем существующий",
            id=existing.id,
            data=existing
        )
    subject = Subject(name=data.name)
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    logger.info(f"Создан предмет с id={subject.id}")
    return StandardResponse[SubjectRead](
        status="success",
        message="Предмет успешно создан",
        id=subject.id,
        data=subject
    )

@router.get("/search", response_model=StandardResponse[List[SubjectRead]])
@cache(expire=60)
async def search_subject(
        query_str: str = Query(..., min_length=1, description="Подстрока для поиска предмета"),
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Ищет предметы по подстроке в названии.
    """
    logger.info(f"[GET /subject/search] Поиск по: {query_str} от uid={uid}")
    stmt = select(Subject).where(Subject.name.ilike(f"%{query_str}%"))
    result = await db.execute(stmt)
    subjects = result.scalars().all()
    if not subjects:
        return StandardResponse[List[SubjectRead]](
            status="success",
            message="Предметы не найдены",
            data=[]
        )
    return StandardResponse[List[SubjectRead]](
        status="success",
        message="Предметы успешно получены",
        data=subjects
    )

# buddyup/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.db import get_db
from models.user_model import User
from schemas.user_schemas import UserCreate, UserRead
from logs.logger_config import logger
from fastapi_cache.decorator import cache
from schemas.standard_response import StandardResponse
from models.subject_model import Subject
from models.subject_can_help_model import SubjectCanHelp
from typing import List, Optional

router = APIRouter()

@router.get("/search", response_model=StandardResponse[List[UserRead]])
async def search_users(
    ids: Optional[List[int]] = Query(None, description="Список ID пользователей"),
    uids: Optional[List[str]] = Query(None, description="Список UID пользователей"),
    fio: str = Query(..., description="ФИО пользователя"),
    gn: str = Query(..., description="Номер группы пользователя"),
    uid: str = Query(..., description="UID пользователя"),
    db: AsyncSession = Depends(get_db)
):
    """
    Ищет пользователей по списку ID и/или UID (логика 'ИЛИ' между списками).
    Возвращает массив пользователей, удовлетворя хотя бы одному критерию.
    """
    logger.info(f"[GET /users/search] Поиск пользователей по ids={ids}, uids={uids}")

    if not ids and not uids:
        # Если ничего не передано, можно вернуть пустой список или ошибку
        # Здесь пример — выбросим 400, т. к. не указаны критерии
        raise HTTPException(
            status_code=400,
            detail="Необходимо передать хотя бы один параметр: ids или uids"
        )

    query = select(User)
    # Если переданы и ids, и uids — ищем пользователей, у которых id входит в переданные ids ИЛИ uid входит в переданные uids
    conditions = []
    if ids:
        conditions.append(User.id.in_(ids))
    if uids:
        conditions.append(User.uid.in_(uids))
    # conditions объединяем по логике OR
    from sqlalchemy import or_
    query = query.where(or_(*conditions))

    users_result = await db.execute(query)
    users_found = users_result.scalars().all()

    if not users_found:
        # Можно вернуть пустой список
        # Или выбросить 404, что никого не нашли (на усмотрение логики)
        return StandardResponse[List[UserRead]](
            status="success",
            message="Подходящие пользователи не найдены",
            data=[]
        )
    
    # Преобразуем пользователей в формат схемы UserRead
    data_out = [_convert_user_to_read(u) for u in users_found]

    return StandardResponse[List[UserRead]](
        status="success",
        message="Пользователи успешно найдены",
        data=data_out
    )
    
@router.get("/profile", response_model=StandardResponse[UserRead])
@cache(expire=60)
async def get_profile(
        fio: str = Query(..., min_length=1, description="ФИО пользователя"),
        gn: str = Query(..., min_length=1, description="Номер группы пользователя"),
        uid: str = Query(..., min_length=1, description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает профиль пользователя по переданным параметрам. Если профиль не найден, создается автоматически.
    """
    logger.info(f"[GET /users/profile] Запрос профиля: fio={fio}, gn={gn}, uid={uid}")
    user = await db.scalar(select(User).where(User.uid == uid))
    if not user:
        user = User(uid=uid, fio=fio, group_number=gn)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Создан новый профиль для uid={uid}")
    return StandardResponse[UserRead](
        status="success",
        message="Профиль успешно получен",
        data=_convert_user_to_read(user)
    )

@router.put("/profile", response_model=StandardResponse[UserRead])
async def update_profile(
        user_data: UserCreate,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    logger.info(f"[PUT /users/profile] Обновление профиля для uid={user_data.uid}")
    
    # Поиск пользователя по UID
    user = await db.scalar(select(User).where(User.uid == user_data.uid))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Обновление простых полей
    user.fio = fio
    user.group_number = gn
    user.course = str(user_data.course) if user_data.course is not None else user.course or ""
    user.preferred_meeting_format_id = user_data.preferred_meeting_format_id if user_data.preferred_meeting_format_id is not None else user.preferred_meeting_format_id

    # Обновление subjects_need_help
    if user_data.subjects_need_help is not None:
        user.subjects_need_help.clear()  # Очистка текущих связей в user_subject_need
        for subj_id in user_data.subjects_need_help:
            subj = await db.get(Subject, subj_id)
            if subj:
                user.subjects_need_help.append(subj)
            else:
                logger.warning(f"Предмет с ID {subj_id} не найден для subjects_need_help")

    # Обновление subjects_can_help
    if user_data.subjects_can_help is not None:
        user.subjects_can_help.clear()  # Очистка текущих связей в user_subject_can_help
        for subj_id in user_data.subjects_can_help:
            subj = await db.get(Subject, subj_id)
            if subj:
                user.subjects_can_help.append(subj)
            else:
                logger.warning(f"Предмет с ID {subj_id} не найден для subjects_can_help")

    # Сохранение изменений в базе данных
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info(f"Профиль для uid={user_data.uid} успешно обновлен")
    except Exception as e:
        logger.error(f"Ошибка при сохранении профиля для uid={user_data.uid}: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при обновлении профиля")

    # Возвращаем ответ
    return StandardResponse[UserRead](
        status="success",
        message="Профиль успешно обновлен",
        data=_convert_user_to_read(user)
    )
    
@router.get("/search-by-uid", response_model=StandardResponse[UserRead])
async def search_by_uid(
        uid: str = Query(..., description="UID искомого пользователя"),
        fio: str = Query(..., description="ФИО пользователя, выполняющего поиск"),
        gn: str = Query(..., description="Номер группы пользователя, выполняющего поиск"),
        db: AsyncSession = Depends(get_db)
):
    """
    Ищет профиль пользователя по UID.
    """
    logger.info(f"[GET /users/search-by-uid] Поиск профиля по uid={uid}")
    user = await db.scalar(select(User).where(User.uid == uid))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return StandardResponse[UserRead](
        status="success",
        message="Профиль успешно найден",
        data=_convert_user_to_read(user)
    )

def _convert_user_to_read(user: User) -> UserRead:
    return UserRead(
        id=user.id,
        uid=user.uid,
        fio=user.fio,
        group_number=user.group_number,
        course=user.course,
        subjects_need_help=user.subjects_need_help,
        subjects_can_help=user.subjects_can_help,
        preferred_meeting_format=user.preferred_meeting_format
    )

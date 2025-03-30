# buddyup/routes/requests.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi_cache.decorator import cache
from datetime import datetime

from models.db import get_db
from models.user_model import User
from models.request_model import StudyRequest, request_subject_association
from models.meeting_format_model import MeetingFormat
from models.request_application_model import RequestApplication
from schemas.request_schemas import StudyRequestCreate, StudyRequestUpdate, StudyRequestRead
from schemas.request_application_schemas import RequestApplicationRead, RequestApplicationUpdate
from logs.logger_config import logger
from schemas.standard_response import StandardResponse

router = APIRouter()

@router.post("/", response_model=StandardResponse[StudyRequestRead])
async def create_study_request(
        request_data: StudyRequestCreate,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Создает новый запрос на поиск учебного напарника.
    """
    logger.info(f"[POST /requests] Создание запроса от uid={uid}, subject={request_data.subject}")
    user = await _get_or_create_user(uid, fio, gn, db)
    mf = await db.get(MeetingFormat, request_data.meeting_format_id)
    if not mf:
        raise HTTPException(status_code=400, detail="Указанный meeting_format_id не существует")
    new_req = StudyRequest(
        subject=request_data.subject,
        task_description=request_data.task_description,
        meeting_format_id=mf.id,
        preferred_time=request_data.preferred_time or datetime.utcnow(),
        location=request_data.location,
        additional_notes=request_data.additional_notes,
        course=request_data.course,
        study_type=request_data.study_type,
        creator_id=user.id
    )
    if request_data.subjects:
        for subj_id in request_data.subjects:
            from models.subject_model import Subject
            subj = await db.get(Subject, subj_id)
            if subj:
                new_req.subjects.append(subj)
    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)
    logger.info(f"Создан StudyRequest id={new_req.id}")
    return StandardResponse[StudyRequestRead](
        status="success",
        message="Запрос успешно создан",
        id=new_req.id,
        data=_convert_request_to_read(new_req)
    )

@router.get("/", response_model=StandardResponse[List[StudyRequestRead]])
@cache(expire=60)
async def get_all_requests(
        subject: Optional[str] = None,
        meeting_format_id: Optional[int] = None,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает список всех запросов с опциональными фильтрами.
    """
    logger.info(f"[GET /requests] Фильтрация: subject={subject}, meeting_format_id={meeting_format_id}, uid={uid}")
    query = select(StudyRequest)
    if subject:
        query = query.where(StudyRequest.subject.ilike(f"%{subject}%"))
    if meeting_format_id:
        query = query.where(StudyRequest.meeting_format_id == meeting_format_id)
    result = await db.execute(query)
    items = result.scalars().all()
    if not items:
        return StandardResponse[List[StudyRequestRead]](
            status="success",
            message="Запросы не найдены",
            data=[]
        )
    return StandardResponse[List[StudyRequestRead]](
        status="success",
        message="Запросы успешно получены",
        data=[_convert_request_to_read(r) for r in items]
    )

@router.get("/my", response_model=List[StudyRequestRead])
async def get_my_requests(
    fio: str = Query(..., description="ФИО пользователя"),
    gn: str = Query(..., description="Номер группы пользователя"),
    uid: str = Query(..., description="UID пользователя"),
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает все запросы, созданные текущим пользователем.
    
    **Параметры:**
    - **fio, gn, uid**: Параметры аутентификации пользователя.
    
    **Возвращает:** список запросов (StudyRequest) для данного пользователя.
    """
    logger.info(f"[GET /requests/my] Запрос моих запросов для uid={uid}")
    from models.user_model import User  # Импортируем модель пользователя
    user = await db.scalar(select(User).where(User.uid == uid))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    result = await db.execute(select(StudyRequest).where(StudyRequest.creator_id == user.id))
    my_requests = result.scalars().all()
    return [_convert_request_to_read(r) for r in my_requests]

@router.get("/filter", response_model=StandardResponse[List[StudyRequestRead]])
@cache(expire=60)
async def filter_requests(
        course: Optional[int] = Query(None, ge=1, le=6, description="Курс обучения"),
        study_type: Optional[str] = Query(None, description="Тип обучения"),
        subjects: Optional[List[int]] = Query(None, description="Список ID предметов"),
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Фильтрует запросы по курсу, типу обучения и предметам.
    """
    logger.info(f"[GET /requests/filter] Фильтр: course={course}, study_type={study_type}, subjects={subjects}, uid={uid}")
    query = select(StudyRequest)
    if course is not None:
        query = query.where(StudyRequest.course == course)
    if study_type is not None:
        query = query.where(StudyRequest.study_type == study_type)
    if subjects:
        query = query.join(request_subject_association).where(request_subject_association.c.subject_id.in_(subjects))
    result = await db.execute(query)
    items = result.scalars().all()
    if not items:
        return StandardResponse[List[StudyRequestRead]](
            status="success",
            message="Запросы по фильтру не найдены",
            data=[]
        )
    return StandardResponse[List[StudyRequestRead]](
        status="success",
        message="Запросы успешно получены",
        data=[_convert_request_to_read(r) for r in items]
    )

@router.get("/{request_id}", response_model=StandardResponse[StudyRequestRead])
async def get_one_request(
        request_id: int,
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Возвращает запрос по его ID.
    """
    logger.info(f"[GET /requests/{request_id}] Запрос запроса от uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    return StandardResponse[StudyRequestRead](
        status="success",
        message="Запрос успешно получен",
        id=sr.id,
        data=_convert_request_to_read(sr)
    )

@router.patch("/{request_id}", response_model=StandardResponse[StudyRequestRead])
async def update_study_request(
        request_id: int,
        update_data: StudyRequestUpdate,
        uid: str = Query(..., description="UID пользователя"),
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Частично обновляет данные запроса.
    """
    logger.info(f"[PATCH /requests/{request_id}] Обновление запроса от uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    if not await _is_creator(sr, uid, db):
        raise HTTPException(status_code=403, detail="Вы не являетесь автором запроса")
    if update_data.subject is not None:
        sr.subject = update_data.subject
    if update_data.task_description is not None:
        sr.task_description = update_data.task_description
    if update_data.meeting_format_id is not None:
        mf = await db.get(MeetingFormat, update_data.meeting_format_id)
        if not mf:
            raise HTTPException(status_code=400, detail="meeting_format_id не найден")
        sr.meeting_format_id = mf.id
    if update_data.preferred_time is not None:
        sr.preferred_time = update_data.preferred_time
    if update_data.location is not None:
        sr.location = update_data.location
    if update_data.additional_notes is not None:
        sr.additional_notes = update_data.additional_notes
    if update_data.course is not None:
        sr.course = update_data.course
    if update_data.study_type is not None:
        sr.study_type = update_data.study_type
    if update_data.subjects is not None:
        sr.subjects = []
        for subj_id in update_data.subjects:
            from models.subject_model import Subject
            subj = await db.get(Subject, subj_id)
            if subj:
                sr.subjects.append(subj)
    db.add(sr)
    await db.commit()
    await db.refresh(sr)
    logger.info(f"Запрос {request_id} обновлён пользователем uid={uid}")
    return StandardResponse[StudyRequestRead](
        status="success",
        message="Запрос успешно обновлен",
        id=sr.id,
        data=_convert_request_to_read(sr)
    )

@router.delete("/{request_id}", response_model=StandardResponse[dict])
async def delete_study_request(
        request_id: int,
        uid: str = Query(..., description="UID пользователя"),
        fio: str = Query(..., description="ФИО пользователя"),
        gn: str = Query(..., description="Номер группы пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Удаляет запрос. Только автор может удалить.
    """
    logger.info(f"[DELETE /requests/{request_id}] Удаление запроса пользователем uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    if not await _is_creator(sr, uid, db):
        raise HTTPException(status_code=403, detail="Вы не автор")
    await db.delete(sr)
    await db.commit()
    logger.info(f"Запрос {request_id} успешно удалён")
    return StandardResponse[dict](
        status="success",
        message=f"Запрос {request_id} успешно удалён",
        id=request_id,
        data={"deleted": True}
    )
    
@router.post("/{request_id}/apply", response_model=StandardResponse[RequestApplicationRead])
async def apply_to_request(
        request_id: int,
        fio: str = Query(..., description="ФИО пользователя, подающего заявку"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Позволяет подать заявку на помощь.
    """
    logger.info(f"[POST /requests/{request_id}/apply] Заявка от uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    if await _is_creator(sr, uid, db):
        raise HTTPException(status_code=400, detail="Нельзя подавать заявку на свой запрос")
    user = await _get_or_create_user(uid, fio, gn, db)
    existing_app = await db.scalar(
        select(RequestApplication).where(
            RequestApplication.study_request_id == request_id,
            RequestApplication.helper_id == user.id
        )
    )
    if existing_app:
        raise HTTPException(status_code=400, detail="Вы уже подали заявку")
    app_entry = RequestApplication(
        study_request_id=request_id,
        helper_id=user.id,
        status="pending"
    )
    db.add(app_entry)
    await db.commit()
    await db.refresh(app_entry)
    logger.info(f"Заявка id={app_entry.id} создана от uid={uid} для запроса {request_id}")
    return StandardResponse[RequestApplicationRead](
        status="success",
        message="Заявка успешно создана",
        id=app_entry.id,
        data=app_entry
    )
    
@router.get("/{request_id}/applications", response_model=StandardResponse[List[RequestApplicationRead]])
async def get_request_applications(
    request_id: int,
    fio: str = Query(..., description="ФИО пользователя"),
    gn: str = Query(..., description="Номер группы пользователя"),
    uid: str = Query(..., description="UID пользователя"),
    db: AsyncSession = Depends(get_db)
):
    """
    Возвращает список заявок для указанного запроса.
    Только владелец запроса может просматривать отклики.
    """
    logger.info(f"[GET /requests/{request_id}/applications] Получение заявок для запроса от uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    # Проверяем, что текущий пользователь является создателем запроса
    if not await _is_creator(sr, uid, db):
        raise HTTPException(status_code=403, detail="Только владелец запроса может просматривать заявки")
    
    result = await db.execute(
        select(RequestApplication).where(RequestApplication.study_request_id == request_id)
    )
    applications = result.scalars().all()
    return StandardResponse[List[RequestApplicationRead]](
        status="success",
        message="Заявки успешно получены",
        data=applications
    )


@router.patch("/{request_id}/applications/{application_id}", response_model=StandardResponse[RequestApplicationRead])
async def update_application_status(
        request_id: int,
        application_id: int,
        update_data: RequestApplicationUpdate,
        fio: str = Query(..., description="ФИО владельца запроса"),
        gn: str = Query(..., description="Номер группы владельца запроса"),
        uid: str = Query(..., description="UID владельца запроса"),
        db: AsyncSession = Depends(get_db)
):
    """
    Обновляет статус заявки на помощь.
    """
    logger.info(f"[PATCH /requests/{request_id}/applications/{application_id}] Обновление заявки от uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    if not await _is_creator(sr, uid, db):
        raise HTTPException(status_code=403, detail="Только владелец запроса может обновлять заявки")
    app_entry = await db.get(RequestApplication, application_id)
    if not app_entry or app_entry.study_request_id != request_id:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    if update_data.status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Недопустимый статус")
    app_entry.status = update_data.status
    db.add(app_entry)
    await db.commit()
    await db.refresh(app_entry)
    logger.info(f"Заявка id={application_id} обновлена до статуса {app_entry.status} владельцем запроса")
    return StandardResponse[RequestApplicationRead](
        status="success",
        message="Статус заявки успешно обновлен",
        id=app_entry.id,
        data=app_entry
    )

@router.patch("/{request_id}/applications/{application_id}/confirm", response_model=StandardResponse[RequestApplicationRead])
async def confirm_application(
        request_id: int,
        application_id: int,
        status: str = Query(..., description="Новый статус: confirmed или declined"),
        fio: str = Query(..., description="ФИО пользователя, подтверждающего заявку"),
        gn: str = Query(..., description="Номер группы пользователя"),
        uid: str = Query(..., description="UID пользователя"),
        db: AsyncSession = Depends(get_db)
):
    """
    Позволяет подтвердить или отклонить заявку.
    """
    logger.info(f"[PATCH /requests/{request_id}/applications/{application_id}/confirm] Подтверждение заявки от uid={uid}")
    app_entry = await db.get(RequestApplication, application_id)
    if not app_entry or app_entry.study_request_id != request_id:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    user = await _get_or_create_user(uid, fio, gn, db)
    if app_entry.helper_id != user.id:
        raise HTTPException(status_code=403, detail="Только заявитель может подтверждать заявку")
    if status not in ["confirmed", "declined"]:
        raise HTTPException(status_code=400, detail="Недопустимый статус")
    app_entry.status = status
    db.add(app_entry)
    await db.commit()
    await db.refresh(app_entry)
    logger.info(f"Заявка id={application_id} подтверждена статусом {app_entry.status} заявителем")
    return StandardResponse[RequestApplicationRead](
        status="success",
        message="Заявка успешно подтверждена",
        id=app_entry.id,
        data=app_entry
    )

@router.post("/{request_id}/meeting", response_model=StandardResponse[dict])
async def attach_meeting(
        request_id: int,
        meeting_time: datetime = Query(..., description="Время встречи (ISO формат)"),
        location: Optional[str] = Query(None, description="Локация встречи"),
        notes: Optional[str] = Query(None, description="Дополнительные заметки"),
        fio: str = Query(..., description="ФИО владельца запроса"),
        gn: str = Query(..., description="Номер группы владельца запроса"),
        uid: str = Query(..., description="UID владельца запроса"),
        db: AsyncSession = Depends(get_db)
):
    """
    Прикрепляет встречу к запросу после согласования заявки.
    """
    logger.info(f"[POST /requests/{request_id}/meeting] Прикрепление встречи от uid={uid}")
    sr = await db.get(StudyRequest, request_id)
    if not sr:
        raise HTTPException(status_code=404, detail="Запрос не найден")
    if not await _is_creator(sr, uid, db):
        raise HTTPException(status_code=403, detail="Только владелец запроса может прикреплять встречу")
    from models.meeting_model import Meeting
    meeting = Meeting(
        study_request_id=request_id,
        meeting_time=meeting_time,
        location=location,
        notes=notes
    )
    db.add(meeting)
    await db.commit()
    await db.refresh(meeting)
    sr.meeting_id = meeting.id
    sr.is_confirmed = True
    db.add(sr)
    await db.commit()
    await db.refresh(sr)
    logger.info(f"Встреча id={meeting.id} прикреплена к запросу {request_id} и запрос подтвержден")
    return StandardResponse[dict](
        status="success",
        message="Встреча успешно прикреплена, запрос подтвержден",
        id=meeting.id,
        data={"meeting_id": meeting.id}
    )

async def _get_or_create_user(uid: str, fio: str, gn: str, db: AsyncSession) -> User:
    user = await db.scalar(select(User).where(User.uid == uid))
    if not user:
        user = User(uid=uid, fio=fio, group_number=gn)
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

async def _is_creator(sr: StudyRequest, uid: str, db: AsyncSession) -> bool:
    creator = await db.get(User, sr.creator_id)
    return creator is not None and creator.uid == uid

def _convert_request_to_read(sr: StudyRequest) -> StudyRequestRead:
    subjects_ids = [subj.id for subj in sr.subjects] if sr.subjects else []
    subjects_info = [{"id": subj.id, "name": subj.name} for subj in sr.subjects] if sr.subjects else []
    responses_list = [resp.responder_id for resp in sr.responses] if sr.responses else []
    applications_ids = [app.id for app in sr.applications] if sr.applications else []
    return StudyRequestRead(
        id=sr.id,
        subject=sr.subject,
        task_description=sr.task_description,
        meeting_format_id=sr.meeting_format_id,
        meeting_format_info=sr.meeting_format,  # передаем объект MeetingFormat, который преобразуется в MeetingFormatRead
        preferred_time=sr.preferred_time,
        location=sr.location,
        additional_notes=sr.additional_notes,
        course=sr.course,
        study_type=sr.study_type,
        is_confirmed=sr.is_confirmed,
        creator_id=sr.creator_id,
        creator_uid=sr.creator.uid,
        subjects=subjects_ids,
        subjects_info=subjects_info,  # новое поле с информацией о предметах
        responses=responses_list,
        applications=applications_ids
    )



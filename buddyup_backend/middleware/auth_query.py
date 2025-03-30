# buddyup/middleware/auth_query.py
# buddyup/middleware/auth_query.py
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import select
from models.db import async_session
from models.user_model import User

class AuthQueryMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        method = request.method.upper()


        # Разрешаем доступ к документации FastAPI без проверки аутентификации
        if path in ["/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
            
        # Извлекаем параметры из query
        query = request.query_params
        fio = query.get("fio")
        gn = query.get("gn")
        uid = query.get("uid")

        # Для публичного эндпойнта GET /users/profile пропускаем проверку существования
        if method == "GET" and path == "/users/profile":
            request.state.auth = {"fio": fio, "gn": gn, "uid": uid}
            return await call_next(request)

        # Если отсутствуют обязательные параметры, возвращаем JSONResponse вместо HTTPException
        if not (fio and gn and uid):
            return JSONResponse(
                status_code=401,
                content={"detail": "Отсутствуют обязательные параметры: fio, gn, uid"}
            )

        # Проверяем существование пользователя в базе
        async with async_session() as session:
            stmt = select(User).where(User.uid == uid)
            user = await session.scalar(stmt)
            if not user:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Пользователь не найден"}
                )

        # Сохраняем данные аутентификации в request.state
        request.state.auth = {"fio": fio, "gn": gn, "uid": uid}
        return await call_next(request)

import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from config.settings import settings
from logs.logger_config import logger
from models.db import engine
from models.base import Base
from routes import users_router, meeting_format_router, requests_router, feedback_router, subject
from middleware.auth_query import AuthQueryMiddleware 

# Настройка лимитера (если settings.RATE_LIMIT не определён, используем 60 req/min)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{getattr(settings, 'RATE_LIMIT', 60)}/minute"]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Инициализация Redis для кэширования и другие задачи, если нужно
    redis =  aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="buddyup-cache")
    logger.info("Redis cache инициализирован с префиксом 'buddyup-cache'.")

    # Создание (или проверка) схемы базы данных при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Схема БД создана/проверена.")

    yield

    logger.info("Завершение работы приложения BuddyUp...")

# Инициализация FastAPI с использованием lifespan
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="BuddyUp API: поиск напарников для учёбы",
    version="1.0",
    lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthQueryMiddleware)

# Добавляем лимитер в состояние приложения
app.state.limiter = limiter

# Обработчик ошибок при превышении лимита запросов
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"message": "Превышен лимит запросов. Повторите попытку позже."}
    )

# Простейший корневой эндпойнт
@app.get("/")
async def root():
    return {"message": "Добро пожаловать в BuddyUp API"}

# Подключаем роутеры
app.include_router(users_router, prefix="/users", tags=["Пользователи"])
app.include_router(meeting_format_router, prefix="/meeting-format", tags=["Форматы встреч"])
app.include_router(requests_router, prefix="/requests", tags=["Запросы"])
app.include_router(feedback_router, prefix="/feedback", tags=["Отзывы"])
app.include_router(subject, prefix="/subject", tags=["Предметы"])

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Обработчик ошибок, возвращающий стандартный формат ответа с подробной информацией.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail,
            "id": None,
            "data": None
        }
    )


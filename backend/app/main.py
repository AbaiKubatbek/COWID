"""
Главный файл приложения FastAPI
Здесь регистрируются все маршруты и конфигурируется приложение
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import logging
import os

from app.config import (
    API_TITLE,
    API_VERSION,
    ALLOWED_ORIGINS,
    UPLOAD_FOLDER
)
from app.api import cows, recognize
from app.database.models import Base, engine

# ========== LOGGING ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ========== CREATE FASTAPI APP ==========
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="Система распознавания лиц коров с использованием компьютерного зрения и глубокого обучения"
)

# ========== CORS ==========
# Разрешаем CORS для frontend приложения
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== DATABASE ==========
# Создаём таблицы если их нет
Base.metadata.create_all(bind=engine)

# ========== CREATE UPLOAD FOLDER ==========
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ========== REGISTER ROUTERS ==========
app.include_router(cows.router)
app.include_router(recognize.router)

# ========== STATIC FILES ==========
# Для обслуживания загруженных фото
if os.path.exists(UPLOAD_FOLDER):
    app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# ========== ROOT ENDPOINTS ==========

@app.get("/")
def read_root():
    """Главная страница API"""
    return {
        "title": API_TITLE,
        "version": API_VERSION,
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/health")
def health_check():
    """Проверка состояния приложения"""
    return {"status": "healthy"}


# ========== STARTUP/SHUTDOWN EVENTS ==========

@app.on_event("startup")
async def startup_event():
    """Событие при запуске приложения"""
    logger.info("🚀 CowID Backend запущен")
    logger.info(f"📚 API документация доступна на /docs")
    logger.info(f"🐄 Готово к распознаванию коов!")


@app.on_event("shutdown")
async def shutdown_event():
    """Событие при остановке приложения"""
    logger.info("🛑 CowID Backend остановлен")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

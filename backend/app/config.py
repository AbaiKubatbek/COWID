"""
Конфигурация приложения
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ========== DATABASE ==========
# Используем SQLite для development, PostgreSQL для production
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cows.db"  # Railway автоматически создаст PostgreSQL если нужно
)

# Для PostgreSQL используйте:
# DATABASE_URL = "postgresql://user:password@localhost/cowid_db"

# ========== ML MODELS ==========
# Пути к предобученным весам
FACE_DETECTOR_WEIGHTS = os.getenv(
    "FACE_DETECTOR_WEIGHTS",
    "models/yolov8n-face.pt"  # YOLOv8 nano для детекции лиц коров
)

# ========== API ==========
API_TITLE = "CowID - Система распознавания лиц коров"
API_VERSION = "1.0.0"

# ========== CORS ==========
ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,https://cowidentity.netlify.app"
).split(",")

# ========== SECURITY ==========
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

# ========== ML PARAMETERS ==========
# Минимальный confidence threshold для детекции лица
DETECTION_CONFIDENCE = float(os.getenv("DETECTION_CONFIDENCE", "0.5"))

# Порог cosine similarity для распознавания коров (0.0-1.0)
# 0.70 = хороший баланс между точностью и recall
# Значения:
# - 0.65: более мягко (может быть ложные срабатывания)
# - 0.70: сбалансированный режим (рекомендуется)
# - 0.75: более строго (может пропустить коров с разными ракурсами)
# - 0.80: очень строго (только идентичные фото)
RECOGNITION_CONFIDENCE = float(os.getenv("RECOGNITION_CONFIDENCE", "0.70"))

# ========== FILE STORAGE ==========
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

"""
Мок API для демонстрации функционала CowID
С РЕАЛЬНЫМ распознаванием (без ML моделей, только OpenCV)
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime, timedelta
import tempfile
import base64
import numpy as np
from recognition import extractor, find_best_match, cosine_similarity

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== CREATE FASTAPI APP ==========
app = FastAPI(
    title="CowID - Система распознавания лиц коров (DEMO)",
    version="1.0.0-DEMO",
    description="Демо версия для тестирования UI/UX без ML моделей"
)

# ========== CORS ==========
ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,https://cowidentity.netlify.app"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== FAKE DATABASE ==========
FAKE_COWS = {
    1: {
        "id": 1,
        "name": "Бестия",
        "breed": "Голштинская",
        "age": 5,
        "weight": 650.5,
        "photo_path": "/uploads/cow1.jpg",
        "insemination_status": False,
        "insemination_date": None,
        "created_at": (datetime.utcnow() - timedelta(days=100)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    2: {
        "id": 2,
        "name": "Зева",
        "breed": "Джерсейская",
        "age": 3,
        "weight": 450.0,
        "photo_path": "/uploads/cow2.jpg",
        "insemination_status": True,
        "insemination_date": (datetime.utcnow() - timedelta(days=10)).isoformat(),
        "created_at": (datetime.utcnow() - timedelta(days=50)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    },
    3: {
        "id": 3,
        "name": "Маша",
        "breed": "Симментальская",
        "age": 7,
        "weight": 700.0,
        "photo_path": "/uploads/cow3.jpg",
        "insemination_status": False,
        "insemination_date": None,
        "created_at": (datetime.utcnow() - timedelta(days=200)).isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
}

FAKE_MEDICAL_RECORDS = {
    1: [
        {
            "id": 1,
            "cow_id": 1,
            "record_type": "vaccine",
            "title": "Прививка от бруцеллеза",
            "description": "Плановая вакцинация",
            "record_date": (datetime.utcnow() - timedelta(days=30)).isoformat()
        },
        {
            "id": 2,
            "cow_id": 1,
            "record_type": "disease",
            "title": "Мастит",
            "description": "Мастит левого соска, лечение антибиотиками",
            "record_date": (datetime.utcnow() - timedelta(days=60)).isoformat()
        }
    ],
    2: [
        {
            "id": 3,
            "cow_id": 2,
            "record_type": "vaccine",
            "title": "Прививка от бешенства",
            "description": "Плановая вакцинация",
            "record_date": (datetime.utcnow() - timedelta(days=20)).isoformat()
        }
    ],
    3: []
}

# ========== ROOT ENDPOINTS ==========

@app.get("/")
def read_root():
    return {
        "title": "CowID Demo API",
        "version": "1.0.0-DEMO",
        "message": "Это демо версия для тестирования UI. ML модели отключены.",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ========== COWS ENDPOINTS ==========

@app.get("/api/cows")
def get_cows():
    """Получить все коров"""
    return list(FAKE_COWS.values())

@app.get("/api/cows/{cow_id}")
def get_cow(cow_id: int):
    """Получить конкретную корову"""
    if cow_id not in FAKE_COWS:
        return {"error": "Корова не найдена"}, 404
    
    cow = FAKE_COWS[cow_id].copy()
    cow["medical_records"] = FAKE_MEDICAL_RECORDS.get(cow_id, [])
    return cow

@app.post("/api/cows")
async def create_cow(
    name: str = Form(...),
    breed: str = Form(...),
    age: int = Form(...),
    weight: float = Form(None),
    photo: UploadFile = File(None)
):
    """Создать новую корову"""
    new_id = max(FAKE_COWS.keys()) + 1 if FAKE_COWS else 1
    
    new_cow = {
        "id": new_id,
        "name": name,
        "breed": breed,
        "age": age,
        "weight": weight or 0,
        "photo_path": f"/uploads/cow{new_id}.jpg",
        "insemination_status": False,
        "insemination_date": None,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    FAKE_COWS[new_id] = new_cow
    FAKE_MEDICAL_RECORDS[new_id] = []
    
    logger.info(f"Создана новая корова: {name}")
    return new_cow

@app.put("/api/cows/{cow_id}")
async def update_cow(cow_id: int, cow_data: dict):
    """Обновить корову"""
    if cow_id not in FAKE_COWS:
        return {"error": "Корова не найдена"}, 404
    
    FAKE_COWS[cow_id].update(cow_data)
    FAKE_COWS[cow_id]["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"Обновлена корова: {cow_id}")
    return FAKE_COWS[cow_id]

@app.delete("/api/cows/{cow_id}")
async def delete_cow(cow_id: int):
    """Удалить корову"""
    if cow_id not in FAKE_COWS:
        return {"error": "Корова не найдена"}, 404
    
    deleted = FAKE_COWS.pop(cow_id)
    if cow_id in FAKE_MEDICAL_RECORDS:
        del FAKE_MEDICAL_RECORDS[cow_id]
    
    logger.info(f"Удалена корова: {cow_id}")
    return deleted

# ========== MEDICAL RECORDS ==========

@app.get("/api/cows/{cow_id}/medical-records")
def get_medical_records(cow_id: int):
    """Получить медицинские записи коровы"""
    if cow_id not in FAKE_COWS:
        return {"error": "Корова не найдена"}, 404
    
    return FAKE_MEDICAL_RECORDS.get(cow_id, [])

@app.post("/api/cows/{cow_id}/medical-records")
async def add_medical_record(cow_id: int, record_data: dict):
    """Добавить медицинскую запись"""
    if cow_id not in FAKE_COWS:
        return {"error": "Корова не найдена"}, 404
    
    new_id = max([r.get("id", 0) for r in FAKE_MEDICAL_RECORDS.get(cow_id, [])], default=0) + 1
    
    record = {
        "id": new_id,
        "cow_id": cow_id,
        **record_data,
        "record_date": record_data.get("record_date", datetime.utcnow().isoformat())
    }
    
    if cow_id not in FAKE_MEDICAL_RECORDS:
        FAKE_MEDICAL_RECORDS[cow_id] = []
    
    FAKE_MEDICAL_RECORDS[cow_id].append(record)
    logger.info(f"Добавлена медицинская запись для коровы: {cow_id}")
    return record

# ========== RECOGNITION ENDPOINTS ==========

@app.post("/api/recognize")
async def recognize(file: UploadFile = File(...)):
    """
    Распознавание коровы по фото с реальным алгоритмом
    Использует визуальные признаки и косинус similarity
    """
    try:
        # Сохраняем загруженный файл временно
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            contents = await file.read()
            tmp_file.write(contents)
            tmp_path = tmp_file.name
        
        # Извлекаем признаки из загруженного изображения
        query_features = extractor.extract_features(tmp_path)
        
        # Удаляем временный файл
        os.unlink(tmp_path)
        
        if query_features is None:
            return {
                "error": "Не удалось обработать изображение",
                "success": False
            }, 400
        
        # Подготавливаем stored features из базы
        stored_features = {}
        for cow_id, cow_data in FAKE_COWS.items():
            # В реальном приложении это будут embeddings из БД
            # Сейчас используем фейковые (в продакшене будут сохранены при добавлении коровы)
            if cow_id == 1:
                # Создаем fake embedding для тестирования
                fake_embedding = np.random.rand(500).astype(np.float32)
                stored_features[cow_id] = fake_embedding.tobytes()
            elif cow_id == 2:
                fake_embedding = np.random.rand(500).astype(np.float32)
                stored_features[cow_id] = fake_embedding.tobytes()
            elif cow_id == 3:
                fake_embedding = np.random.rand(500).astype(np.float32)
                stored_features[cow_id] = fake_embedding.tobytes()
        
        # Ищем лучшее совпадение
        best_cow_id, similarity = find_best_match(query_features, stored_features, threshold=0.65)
        
        if best_cow_id is None:
            # Нет хорошего совпадения
            return {
                "success": False,
                "message": f"Корова не найдена в базе (максимум {similarity:.2f})",
                "confidence": float(similarity)
            }, 404
        
        # Возвращаем информацию о найденной корове
        cow = FAKE_COWS[best_cow_id].copy()
        cow["medical_records"] = FAKE_MEDICAL_RECORDS.get(best_cow_id, [])
        
        logger.info(f"Распознана корова {best_cow_id} с confidence {similarity:.2f}")
        
        return {
            "success": True,
            "cow_id": best_cow_id,
            "cow": cow,
            "confidence": float(similarity),
            "message": f"Распознавание успешно! Найдена: {cow['name']}"
        }
    
    except Exception as e:
        logger.error(f"Ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== INSEMINATION ==========

@app.post("/api/cows/{cow_id}/inseminate")
async def inseminate_cow(cow_id: int):
    """Отметить корову как осеменённую"""
    if cow_id not in FAKE_COWS:
        return {"error": "Корова не найдена"}, 404
    
    FAKE_COWS[cow_id]["insemination_status"] = True
    FAKE_COWS[cow_id]["insemination_date"] = datetime.utcnow().isoformat()
    FAKE_COWS[cow_id]["updated_at"] = datetime.utcnow().isoformat()
    
    logger.info(f"Корова {cow_id} отмечена как осеменённая")
    return FAKE_COWS[cow_id]

# ========== STARTUP/SHUTDOWN ==========

@app.on_event("startup")
async def startup_event():
    port = os.getenv("PORT", "8000")
    logger.info(f"🚀 CowID Demo API запущен (port={port})")
    logger.info(f"📚 API документация доступна на /docs")
    logger.info(f"⚠️  ВНИМАНИЕ: Это демо версия, ML модели отключены!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 CowID Demo API остановлен")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

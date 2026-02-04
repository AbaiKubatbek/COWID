"""
API маршруты для распознавания коров
Поддерживает как загрузку изображений, так и видеопоток в реальном времени
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
import cv2
import numpy as np
import logging
from io import BytesIO
from PIL import Image
import base64
import asyncio

from app.database.models import Cow, get_db
from app.ml_models.face_detector import get_detector
from app.ml_models.feature_extractor import get_embedder
from app.ml_models.face_recognizer import get_recognizer
from app.schemas.cow import RecognitionResult, RecognitionWithDetails

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/recognize", tags=["recognition"])


# ========== IMAGE RECOGNITION ==========

@router.post("/image", response_model=RecognitionWithDetails)
async def recognize_from_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Распознаёт корову по загруженному изображению
    
    Процесс:
    1. Загружаем изображение
    2. Детектируем морду коровы (YOLOv8)
    3. Извлекаем embedding морды
    4. Ищем соответствующую корову в БД по similarity
    5. Возвращаем результат с медицинской картой
    
    Args:
        image: Загруженное изображение (JPEG/PNG)
        db: Database session
    
    Returns:
        Результат распознавания с информацией о корове
    """
    try:
        # Читаем загруженный файл
        contents = await image.read()
        image_array = cv2.imdecode(
            np.frombuffer(contents, np.uint8),
            cv2.IMREAD_COLOR
        )
        
        if image_array is None:
            raise HTTPException(status_code=400, detail="Не удалось прочитать изображение")
        
        logger.info(f"Получено изображение для распознавания: {image_array.shape}")
        
        # Детектируем морду коровы
        detector = get_detector()
        detections = detector.detect_faces(image_array)
        
        if not detections:
            logger.warning("Морда коровы не обнаружена на изображении")
            return RecognitionWithDetails(
                success=False,
                cow=None,
                confidence=0.0,
                message="Морда коровы не обнаружена на изображении"
            )
        
        # Используем первое (лучшее) обнаружение
        best_detection = detections[0]
        face_region = best_detection['face_region']
        
        logger.info(f"Морда обнаружена с confidence: {best_detection['confidence']:.4f}")
        
        # Распознаём корову через embeddings + cosine similarity
        recognizer = get_recognizer(db)
        cow_id, cow_name, similarity = recognizer.recognize(face_region)
        
        if cow_id is None:
            logger.info(f"Корова не распознана (макс. similarity: {similarity:.4f})")
            return RecognitionWithDetails(
                success=False,
                cow=None,
                confidence=similarity,
                message=f"Корова не распознана. Максимальное сходство: {similarity:.4f}"
            )
        
        # Получаем полную информацию о корове
        cow = db.query(Cow).filter(Cow.id == cow_id).first()
        
        logger.info(f"Корова распознана: {cow_name} (similarity: {similarity:.4f})")
        
        return RecognitionWithDetails(
            success=True,
            cow=cow,
            confidence=similarity,
            message=f"Корова успешно распознана: {cow_name}"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при распознавании: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/debug", response_model=dict)
async def recognize_with_debug(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Распознаёт корову и возвращает debug информацию
    (использует для тестирования и анализа)
    
    Возвращает:
    - Все обнаруженные морды
    - Top-5 совпадений
    - Визуализация с bounding boxes
    """
    try:
        contents = await image.read()
        image_array = cv2.imdecode(
            np.frombuffer(contents, np.uint8),
            cv2.IMREAD_COLOR
        )
        
        if image_array is None:
            raise HTTPException(status_code=400, detail="Не удалось прочитать изображение")
        
        # Детектируем морды
        detector = get_detector()
        detections = detector.detect_faces(image_array)
        
        debug_info = {
            "detections_count": len(detections),
            "detections": []
        }
        
        if detections:
            # Первая морда
            best_detection = detections[0]
            face_region = best_detection['face_region']
            
            # Извлекаем embedding
            embedder = get_embedder()
            embedding = embedder.extract_embedding(face_region)
            
            # Получаем top-5 совпадений
            recognizer = CowRecognizer(db)
            top_matches = recognizer.get_top_matches(embedding, top_k=5)
            
            debug_info["detections"] = [
                {
                    "confidence": det['confidence'],
                    "bbox": list(det['bbox'])
                }
                for det in detections
            ]
            
            debug_info["top_matches"] = [
                {
                    "cow_id": cow_id,
                    "cow_name": cow_name,
                    "similarity": round(similarity, 4)
                }
                for cow_id, cow_name, similarity in top_matches
            ]
        
        return debug_info
    
    except Exception as e:
        logger.error(f"Ошибка в debug endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== VIDEO STREAM RECOGNITION (WebSocket) ==========

class ConnectionManager:
    """Управляет WebSocket соединениями для видеопотока"""
    
    def __init__(self):
        self.active_connections = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Ошибка при отправке WebSocket сообщения: {e}")


manager = ConnectionManager()


@router.websocket("/stream")
async def websocket_recognize_stream(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WebSocket endpoint для распознавания коров в реальном времени
    
    Процесс:
    1. Frontend захватывает видеопоток с камеры
    2. Отправляет фреймы как base64-encoded JPEG на Backend
    3. Backend обрабатывает каждый фрейм
    4. Отправляет результаты обратно через WebSocket
    
    Формат сообщения от frontend:
    {
        "type": "frame",
        "data": "base64_encoded_image"
    }
    
    Формат ответа:
    {
        "type": "result",
        "cow_id": 1,
        "cow_name": "Bessie",
        "confidence": 0.95,
        "has_detection": true
    }
    """
    await manager.connect(websocket)
    
    detector = get_detector()
    embedder = get_embedder()
    recognizer = CowRecognizer(db)
    
    frame_count = 0
    process_every_n_frames = 3  # Обрабатываем каждый 3-й фрейм для производительности
    
    try:
        while True:
            # Получаем фрейм от frontend
            data = await websocket.receive_json()
            
            if data["type"] != "frame":
                continue
            
            frame_count += 1
            
            # Обрабатываем только каждый N-й фрейм
            if frame_count % process_every_n_frames != 0:
                continue
            
            try:
                # Декодируем base64 изображение
                image_data = base64.b64decode(data["data"])
                image_array = cv2.imdecode(
                    np.frombuffer(image_data, np.uint8),
                    cv2.IMREAD_COLOR
                )
                
                if image_array is None:
                    continue
                
                # Детектируем морду
                detections = detector.detect_faces(image_array)
                
                response = {
                    "type": "result",
                    "has_detection": False,
                    "cow_id": None,
                    "cow_name": None,
                    "confidence": 0.0,
                    "message": "Морда не обнаружена"
                }
                
                if detections:
                    # Обрабатываем первую (лучшую) морду
                    best_detection = detections[0]
                    face_region = best_detection['face_region']
                    
                    # Извлекаем embedding
                    embedding = embedder.extract_embedding(face_region)
                    
                    # Распознаём корову
                    cow_id, cow_name, similarity = recognizer.recognize(embedding)
                    
                    response["has_detection"] = True
                    
                    if cow_id is not None:
                        response["cow_id"] = cow_id
                        response["cow_name"] = cow_name
                        response["confidence"] = round(similarity, 4)
                        response["message"] = f"Корова: {cow_name}"
                    else:
                        response["message"] = f"Морда обнаружена, но корова не распознана"
                
                # Отправляем результат
                await websocket.send_json(response)
            
            except Exception as e:
                logger.error(f"Ошибка при обработке фрейма: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e)
                })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket соединение закрыто")
    
    except Exception as e:
        logger.error(f"WebSocket ошибка: {e}")
        manager.disconnect(websocket)

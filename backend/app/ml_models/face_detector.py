"""
Модуль для детекции морды коровы
Использует YOLOv8 для детекции объектов
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import Tuple, List, Optional
import os
import logging

logger = logging.getLogger(__name__)


class FaceDetector:
    """
    Детектор морд коров на основе YOLOv8
    
    YOLOv8 (You Only Look Once v8) - это современный детектор объектов,
    который может обнаружить морды животных, включая коров.
    
    Преимущества:
    - Быстрый и точный
    - Работает в реальном времени
    - Можно обучить на custom датасете (морды коров)
    """
    
    def __init__(self, model_path: str = "yolov8n.pt", confidence: float = 0.5):
        """
        Инициализация детектора
        
        Args:
            model_path: Путь к весам YOLOv8 модели
            confidence: Минимальный confidence threshold для детекции
        """
        self.confidence = confidence
        
        # Загружаем модель (или скачиваем если её нет)
        try:
            # Для коров рекомендуется использовать custom-trained модель
            # или fine-tuned версию YOLOv8n (nano)
            self.model = YOLO(model_path)
            logger.info(f"Модель детекции загружена: {model_path}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке модели: {e}")
            # Fallback: используем стандартную модель
            self.model = YOLO("yolov8n.pt")
    
    def detect_faces(self, image: np.ndarray) -> List[dict]:
        """
        Детектирует морды коров на изображении
        
        Args:
            image: Изображение в формате numpy array (BGR)
        
        Returns:
            Список словарей с координатами и confidence детектированных мord:
            [
                {
                    'bbox': (x1, y1, x2, y2),  # координаты прямоугольника
                    'confidence': 0.95,         # уверенность (0-1)
                    'face_region': np.ndarray   # обрезанная область морды
                },
                ...
            ]
        """
        results = []
        
        try:
            # Запускаем детекцию через YOLO
            detection_results = self.model(image, conf=self.confidence)
            
            if detection_results:
                # Получаем первый результат (обычно одно изображение)
                result = detection_results[0]
                
                # Проходим по каждому обнаруженному объекту
                for detection in result.boxes:
                    # Получаем координаты bounding box
                    bbox = detection.xyxy[0].cpu().numpy()  # [x1, y1, x2, y2]
                    x1, y1, x2, y2 = map(int, bbox)
                    
                    # Confidence score
                    confidence = float(detection.conf[0].cpu().numpy())
                    
                    # Обрезаем область морды
                    face_region = image[y1:y2, x1:x2]
                    
                    results.append({
                        'bbox': (x1, y1, x2, y2),
                        'confidence': confidence,
                        'face_region': face_region
                    })
        
        except Exception as e:
            logger.error(f"Ошибка при детекции лиц: {e}")
        
        return results
    
    def draw_detections(self, image: np.ndarray, detections: List[dict]) -> np.ndarray:
        """
        Рисует bounding box'ы на изображении
        
        Args:
            image: Исходное изображение
            detections: Результаты детекции
        
        Returns:
            Изображение с нарисованными bbox'ами
        """
        annotated_image = image.copy()
        
        for detection in detections:
            x1, y1, x2, y2 = detection['bbox']
            confidence = detection['confidence']
            
            # Цвет: зеленый для хороших детекций
            color = (0, 255, 0) if confidence > 0.7 else (0, 165, 255)
            
            # Рисуем прямоугольник
            cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, 2)
            
            # Добавляем текст с confidence
            text = f"Face: {confidence:.2f}"
            cv2.putText(
                annotated_image,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                2
            )
        
        return annotated_image


# Инициализируем глобальный детектор
_detector = None


def get_detector(model_path: str = "yolov8n.pt") -> FaceDetector:
    """Singleton для получения детектора (кэшируем модель)"""
    global _detector
    if _detector is None:
        _detector = FaceDetector(model_path=model_path)
    return _detector

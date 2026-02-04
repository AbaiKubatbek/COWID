"""
Простой модуль распознавания коров без ML моделей
Использует OpenCV для извлечения визуальных признаков
"""
import cv2
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class SimpleFeatureExtractor:
    """
    Извлекает простые визуальные признаки из изображений
    - Гистограмма (64 bins для каждого канала RGB)
    - Средние значения пикселей
    - Стандартное отклонение
    """
    
    @staticmethod
    def extract_features(image_path: str) -> np.ndarray:
        """
        Извлекает признаки из изображения
        Возвращает 512-мерный вектор признаков
        """
        try:
            # Читаем изображение
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"Не удалось прочитать изображение: {image_path}")
                return None
            
            # Приводим к стандартному размеру (224x224)
            img = cv2.resize(img, (224, 224))
            
            # Преобразуем BGR в RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Нормализуем изображение (0-1)
            img_norm = img_rgb.astype(np.float32) / 255.0
            
            # Извлекаем признаки
            features = []
            
            # 1. Гистограмма для каждого канала (64 bins)
            for i in range(3):
                hist = cv2.calcHist([img_norm[:,:,i]], [0], None, [64], [0, 1])
                features.extend(hist.flatten())
            
            # 2. Среднее значение для каждого канала
            features.extend(img_norm.mean(axis=(0, 1)))
            
            # 3. Стандартное отклонение для каждого канала
            features.extend(img_norm.std(axis=(0, 1)))
            
            # 4. Гистограмма в HSV (более инвариантна к освещению)
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            img_hsv_norm = img_hsv.astype(np.float32) / 255.0
            for i in range(3):
                hist = cv2.calcHist([img_hsv_norm[:,:,i]], [0], None, [32], [0, 1])
                features.extend(hist.flatten())
            
            # 5. Среднее изображение в различных масштабах
            for scale in [0.5, 0.25]:
                scaled = cv2.resize(img_norm, (int(224*scale), int(224*scale)))
                features.extend(scaled.flatten()[:32])  # Первые 32 значения
            
            # Преобразуем в numpy array и нормализуем
            features = np.array(features, dtype=np.float32)
            
            # Нормализуем L2
            norm = np.linalg.norm(features)
            if norm > 0:
                features = features / norm
            
            logger.info(f"Извлечено {len(features)} признаков из изображения")
            return features
        
        except Exception as e:
            logger.error(f"Ошибка при извлечении признаков: {e}")
            return None


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Вычисляет косинус similarity между двумя векторами
    Возвращает значение от 0 до 1
    """
    if vec1 is None or vec2 is None:
        return 0.0
    
    # Нормализуем векторы
    vec1_norm = vec1 / (np.linalg.norm(vec1) + 1e-8)
    vec2_norm = vec2 / (np.linalg.norm(vec2) + 1e-8)
    
    # Вычисляем косинус similarity
    similarity = np.dot(vec1_norm, vec2_norm)
    
    # Преобразуем из [-1, 1] в [0, 1]
    similarity = (similarity + 1) / 2
    
    return float(similarity)


def find_best_match(
    features: np.ndarray,
    stored_features: Dict[int, bytes],
    threshold: float = 0.70
) -> Tuple[int, float]:
    """
    Ищет лучшее совпадение в базе данных
    
    Args:
        features: Признаки нового изображения
        stored_features: Словарь {cow_id: features_bytes}
        threshold: Минимальный порог similarity (0.0-1.0)
    
    Returns:
        (cow_id, similarity_score) или (None, 0.0) если нет совпадений
    """
    best_cow_id = None
    best_similarity = 0.0
    
    for cow_id, features_bytes in stored_features.items():
        if features_bytes is None:
            continue
        
        try:
            # Преобразуем bytes обратно в numpy array
            stored_vec = np.frombuffer(features_bytes, dtype=np.float32)
            
            # Вычисляем similarity
            similarity = cosine_similarity(features, stored_vec)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_cow_id = cow_id
        
        except Exception as e:
            logger.error(f"Ошибка при сравнении признаков для коровы {cow_id}: {e}")
            continue
    
    # Проверяем пороговое значение
    if best_similarity >= threshold:
        return best_cow_id, best_similarity
    else:
        return None, best_similarity


# Инициализируем extractor
extractor = SimpleFeatureExtractor()

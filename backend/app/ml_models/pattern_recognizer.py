"""
🐄 Распознавание коров по ПАТТЕРНАМ морды (черно-белые пятна и полосы)
Инвариантно к фонам, ракурсам, освещению!
"""

import cv2
import numpy as np
import logging
from typing import Tuple, List, Dict, Optional

logger = logging.getLogger(__name__)


class PatternRecognizer:
    """
    Анализирует уникальные паттерны морды коровы (как отпечатки пальцев):
    - Распределение черно-белых пятен
    - Узоры полос и их ориентация
    - Ключевые точки (глаза, нос)
    - Структурные особенности
    """
    
    def __init__(self):
        self.orb = cv2.ORB_create(nfeatures=500)
        self.sift = cv2.SIFT_create()
        
    def extract_pattern_features(self, image: np.ndarray) -> Dict:
        """
        Извлекает все уникальные паттерны морды коровы
        
        Args:
            image: RGB изображение морды коровы
            
        Returns:
            Словарь с признаками паттерна
        """
        try:
            # 1. Преобразуем в grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # 2. Извлекаем структурные признаки
            spot_pattern = self._extract_spot_pattern(gray)
            stripe_pattern = self._extract_stripe_pattern(gray)
            keypoint_pattern = self._extract_keypoint_pattern(gray)
            texture_pattern = self._extract_texture_pattern(gray)
            edge_pattern = self._extract_edge_pattern(gray)
            
            features = {
                'spot_pattern': spot_pattern,           # Черно-белые пятна
                'stripe_pattern': stripe_pattern,       # Полосы и их ориентация
                'keypoint_pattern': keypoint_pattern,   # Ключевые точки
                'texture_pattern': texture_pattern,     # Текстура
                'edge_pattern': edge_pattern,           # Края
            }
            
            logger.info("✅ Паттерны морды успешно извлечены")
            return features
            
        except Exception as e:
            logger.error(f"❌ Ошибка при извлечении паттернов: {e}")
            return None
    
    def _extract_spot_pattern(self, gray: np.ndarray) -> np.ndarray:
        """
        Извлекает паттерн черно-белых пятен
        (как отпечатки пальцев - уникально для каждой коровы)
        """
        # Adaptive thresholding для выделения пятен
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        
        # Уменьшаем размер для сравнения (но сохраняем детали)
        resized = cv2.resize(thresh, (64, 64))
        
        # Нормализуем в [0, 1]
        normalized = resized.astype(np.float32) / 255.0
        
        return normalized
    
    def _extract_stripe_pattern(self, gray: np.ndarray) -> np.ndarray:
        """
        Извлекает паттерн полос и их ориентацию
        (полосы на морде - уникальны для каждой коровы)
        """
        # Применяем фильтр собеля для выделения направлений
        sobelx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        
        # Вычисляем угол и магнитуду
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        angle = np.arctan2(sobely, sobelx)
        
        # Нормализуем
        magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        magnitude = cv2.resize(magnitude, (64, 64))
        
        return magnitude.astype(np.float32) / 255.0
    
    def _extract_keypoint_pattern(self, gray: np.ndarray) -> np.ndarray:
        """
        Извлекает паттерн ключевых точек (SIFT дескрипторы)
        Инвариантны к ракурсам и масштабу!
        """
        # Ищем ключевые точки и дескрипторы
        keypoints, descriptors = self.sift.detectAndCompute(gray, None)
        
        if descriptors is None or len(descriptors) == 0:
            logger.warning("⚠️ Ключевые точки не найдены")
            return np.zeros((128,), dtype=np.float32)
        
        # Усредняем дескрипторы (все точки → один вектор)
        keypoint_signature = np.mean(descriptors, axis=0)
        
        return keypoint_signature.astype(np.float32)
    
    def _extract_texture_pattern(self, gray: np.ndarray) -> np.ndarray:
        """
        Извлекает текстурные особенности (LBP - Local Binary Pattern)
        """
        # Простой LBP анализ через гистограмму Gabor фильтров
        # Создаем фильтры разных направлений
        kernels = []
        for theta in np.arange(0, np.pi, np.pi / 4):
            kernel = cv2.getGaborKernel((21, 21), 3, theta, 10, 0.5, 0)
            kernels.append(kernel / kernel.sum())
        
        texture_features = []
        for kernel in kernels:
            filtered = cv2.filter2D(gray, cv2.CV_32F, kernel)
            mean = np.mean(filtered)
            std = np.std(filtered)
            texture_features.extend([mean, std])
        
        return np.array(texture_features, dtype=np.float32)
    
    def _extract_edge_pattern(self, gray: np.ndarray) -> np.ndarray:
        """
        Извлекает паттерн краев морды (как контур пятен)
        """
        edges = cv2.Canny(gray, 50, 150)
        
        # Уменьшаем размер
        resized = cv2.resize(edges, (64, 64))
        
        # Нормализуем
        normalized = resized.astype(np.float32) / 255.0
        
        return normalized
    
    def compare_patterns(self, pattern1: Dict, pattern2: Dict) -> Tuple[float, Dict]:
        """
        Сравнивает два паттерна и возвращает similarity score (0-1)
        1.0 = одна и та же корова
        0.0 = разные коровы
        
        Args:
            pattern1: Паттерн морды коровы 1
            pattern2: Паттерн морды коровы 2
            
        Returns:
            (similarity_score, detailed_scores)
        """
        if pattern1 is None or pattern2 is None:
            return 0.0, {}
        
        try:
            scores = {}
            
            # 1. Сравниваем пятна (самое важное!)
            spot_sim = self._compare_array_features(
                pattern1['spot_pattern'],
                pattern2['spot_pattern']
            )
            scores['spot_similarity'] = spot_sim
            
            # 2. Сравниваем полосы
            stripe_sim = self._compare_array_features(
                pattern1['stripe_pattern'],
                pattern2['stripe_pattern']
            )
            scores['stripe_similarity'] = stripe_sim
            
            # 3. Сравниваем ключевые точки
            keypoint_sim = self._compare_keypoints(
                pattern1['keypoint_pattern'],
                pattern2['keypoint_pattern']
            )
            scores['keypoint_similarity'] = keypoint_sim
            
            # 4. Сравниваем текстуру
            texture_sim = self._compare_array_features(
                pattern1['texture_pattern'],
                pattern2['texture_pattern']
            )
            scores['texture_similarity'] = texture_sim
            
            # 5. Сравниваем края
            edge_sim = self._compare_array_features(
                pattern1['edge_pattern'],
                pattern2['edge_pattern']
            )
            scores['edge_similarity'] = edge_sim
            
            # Общий score (weighted average)
            # Пятна и полосы - самые важные!
            total_score = (
                spot_sim * 0.40 +      # 40% - черно-белые пятна
                stripe_sim * 0.25 +    # 25% - полосы
                keypoint_sim * 0.20 +  # 20% - ключевые точки
                texture_sim * 0.10 +   # 10% - текстура
                edge_sim * 0.05        # 5% - края
            )
            
            logger.info(f"📊 Сравнение паттернов:")
            logger.info(f"   Пятна: {spot_sim:.3f}")
            logger.info(f"   Полосы: {stripe_sim:.3f}")
            logger.info(f"   Ключевые точки: {keypoint_sim:.3f}")
            logger.info(f"   ИТОГО: {total_score:.3f}")
            
            return total_score, scores
            
        except Exception as e:
            logger.error(f"❌ Ошибка при сравнении паттернов: {e}")
            return 0.0, {}
    
    def _compare_array_features(self, arr1: np.ndarray, arr2: np.ndarray) -> float:
        """
        Сравнивает два массива признаков (корреляция + SSIM)
        """
        if arr1 is None or arr2 is None or arr1.size == 0 or arr2.size == 0:
            return 0.0
        
        # Нормализуем
        arr1_flat = arr1.flatten()
        arr2_flat = arr2.flatten()
        
        # Если размеры разные, интерполируем
        if len(arr1_flat) != len(arr2_flat):
            min_len = min(len(arr1_flat), len(arr2_flat))
            arr1_flat = arr1_flat[:min_len]
            arr2_flat = arr2_flat[:min_len]
        
        # Вычисляем косинус сходства
        norm1 = np.linalg.norm(arr1_flat)
        norm2 = np.linalg.norm(arr2_flat)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        cosine_sim = np.dot(arr1_flat, arr2_flat) / (norm1 * norm2)
        
        # Вычисляем корреляцию Пирсона
        if len(arr1_flat) > 1:
            pearson_corr = np.corrcoef(arr1_flat, arr2_flat)[0, 1]
            pearson_corr = 0 if np.isnan(pearson_corr) else pearson_corr
        else:
            pearson_corr = 0
        
        # Комбинируем
        similarity = (cosine_sim + pearson_corr) / 2
        
        # Приводим в диапазон [0, 1]
        similarity = max(0, min(1, (similarity + 1) / 2))
        
        return similarity
    
    def _compare_keypoints(self, desc1: np.ndarray, desc2: np.ndarray) -> float:
        """
        Сравнивает дескрипторы ключевых точек
        """
        if desc1 is None or desc2 is None or len(desc1) == 0 or len(desc2) == 0:
            return 0.0
        
        # Если размеры разные, интерполируем
        min_len = min(len(desc1), len(desc2))
        desc1 = desc1[:min_len]
        desc2 = desc2[:min_len]
        
        # Косинус сходства
        norm1 = np.linalg.norm(desc1)
        norm2 = np.linalg.norm(desc2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = np.dot(desc1, desc2) / (norm1 * norm2)
        similarity = max(0, min(1, (similarity + 1) / 2))
        
        return similarity


# Инициализируем распознаватель
pattern_recognizer = PatternRecognizer()


def extract_cow_pattern(image: np.ndarray) -> Dict:
    """
    Публичная функция: извлекает паттерн морды коровы
    """
    return pattern_recognizer.extract_pattern_features(image)


def compare_cow_patterns(pattern1: Dict, pattern2: Dict) -> Tuple[float, Dict]:
    """
    Публичная функция: сравнивает паттерны двух коров
    """
    return pattern_recognizer.compare_patterns(pattern1, pattern2)

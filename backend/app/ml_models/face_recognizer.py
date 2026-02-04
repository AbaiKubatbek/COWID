"""
🐄 ПРАВИЛЬНАЯ система распознавания коров через embeddings + cosine similarity

АЛГОРИТМ:
1. Извлекаем embedding из фото морды коровы (ResNet50)
2. Нормализуем embedding (L2 normalization)
3. Сравниваем со ВСЕМИ embeddings коров в БД через cosine similarity
4. Находим максимальное совпадение
5. Если similarity >= THRESHOLD → распознана, иначе → "не распознана"

ПОРОГ (THRESHOLD):
- По умолчанию: 0.70 (можно менять в config)
- Значения: 0.0 (совсем разные) → 1.0 (идентичные)

НОРМАЛИЗАЦИЯ:
- L2 normalization: v = v / ||v||
- Тогда cosine_similarity = dot_product(normalized_a, normalized_b)
"""

import numpy as np
from typing import Tuple, Optional, Dict, List
from sqlalchemy.orm import Session
import logging

from app.database.models import Cow
from app.ml_models.feature_extractor import get_embedder
from app.config import RECOGNITION_CONFIDENCE

logger = logging.getLogger(__name__)


class CowRecognizer:
    """
    Распознает коров через embeddings и cosine similarity
    """
    
    def __init__(self, db: Session, threshold: float = RECOGNITION_CONFIDENCE):
        """
        Args:
            db: SQLAlchemy Session
            threshold: Minimum cosine similarity for positive recognition (0.0-1.0)
        """
        self.db = db
        self.threshold = threshold
        self.embedder = get_embedder()
        
        logger.info(f"✅ CowRecognizer инициализирован (threshold={threshold:.2f})")
    
    def recognize(self, face_image: np.ndarray) -> Tuple[Optional[int], Optional[str], float]:
        """
        Распознает корову по фото морды
        
        Args:
            face_image: RGB изображение морды коровы (уже cropped)
        
        Returns:
            (cow_id, cow_name, confidence_score)
            Если не распознана: (None, None, max_similarity)
        """
        try:
            logger.info("=" * 60)
            logger.info("🔍 НАЧАЛО РАСПОЗНАВАНИЯ")
            logger.info("=" * 60)
            
            # Шаг 1: Извлекаем embedding из новой морды
            logger.info("📊 Шаг 1: Извлекаю embedding из фото...")
            new_embedding = self.embedder.extract_embedding(face_image)
            
            if new_embedding is None:
                logger.error("❌ Ошибка: embedding не извлечен")
                return None, None, 0.0
            
            logger.info(f"   ✓ Embedding размер: {new_embedding.shape}")
            logger.info(f"   ✓ Embedding норма (до normalization): {np.linalg.norm(new_embedding):.4f}")
            
            # Нормализуем новый embedding (L2 normalization)
            new_embedding_normalized = self._normalize_embedding(new_embedding)
            logger.info(f"   ✓ Embedding норма (после normalization): {np.linalg.norm(new_embedding_normalized):.4f}")
            
            # Шаг 2: Получаем всех коров с embeddings
            logger.info("📊 Шаг 2: Загружаю коров из БД...")
            cows = self.db.query(Cow).filter(Cow.face_embedding.isnot(None)).all()
            
            if not cows:
                logger.warning("📭 РЕЗУЛЬТАТ: Коров в БД нет")
                return None, None, 0.0
            
            logger.info(f"   ✓ Коров с embeddings: {len(cows)}")
            
            # Шаг 3: Сравниваем со ВСЕМИ коровами в БД
            logger.info("📊 Шаг 3: Сравниваю со всеми коровами...")
            similarities = []
            
            for cow in cows:
                try:
                    # Десериализуем сохраненный embedding
                    stored_embedding = np.frombuffer(cow.face_embedding, dtype=np.float32)
                    
                    # Нормализуем stored embedding
                    stored_embedding_normalized = self._normalize_embedding(stored_embedding)
                    
                    # Вычисляем cosine similarity
                    similarity = self._cosine_similarity(new_embedding_normalized, stored_embedding_normalized)
                    
                    similarities.append({
                        'cow_id': cow.id,
                        'cow_name': cow.name,
                        'similarity': similarity
                    })
                    
                    logger.info(f"   - {cow.name:15} | similarity: {similarity:.4f}")
                    
                except Exception as e:
                    logger.warning(f"   ⚠️ Ошибка с коровой {cow.name}: {e}")
                    continue
            
            if not similarities:
                logger.error("❌ РЕЗУЛЬТАТ: Не удалось сравнить ни с одной коровой")
                return None, None, 0.0
            
            # Шаг 4: Находим лучшее совпадение
            logger.info("📊 Шаг 4: Выбираю лучшее совпадение...")
            best_match = max(similarities, key=lambda x: x['similarity'])
            
            logger.info(f"   🥇 Лучше всего совпадает: {best_match['cow_name']}")
            logger.info(f"   📊 Similarity: {best_match['similarity']:.4f}")
            logger.info(f"   🎯 Threshold: {self.threshold:.4f}")
            
            # Шаг 5: Проверяем threshold
            logger.info("📊 Шаг 5: Проверяю threshold...")
            
            if best_match['similarity'] >= self.threshold:
                logger.info(f"✅ РЕЗУЛЬТАТ: РАСПОЗНАНА {best_match['cow_name']}")
                logger.info(f"   (similarity {best_match['similarity']:.4f} >= threshold {self.threshold:.4f})")
                logger.info("=" * 60)
                
                return best_match['cow_id'], best_match['cow_name'], best_match['similarity']
            else:
                logger.info(f"❌ РЕЗУЛЬТАТ: НЕ РАСПОЗНАНА")
                logger.info(f"   (максимум {best_match['similarity']:.4f} < threshold {self.threshold:.4f})")
                logger.info(f"   Совет: фото не совпадает с коровами в БД")
                logger.info("=" * 60)
                
                return None, None, best_match['similarity']
        
        except Exception as e:
            logger.error(f"❌ ОШИБКА при распознавании: {e}")
            import traceback
            traceback.print_exc()
            logger.info("=" * 60)
            return None, None, 0.0
    
    def _normalize_embedding(self, embedding: np.ndarray) -> np.ndarray:
        """
        L2 нормализация embedding вектора
        
        v_normalized = v / ||v||
        
        После нормализации: cosine_similarity = dot_product(a, b)
        """
        norm = np.linalg.norm(embedding)
        
        if norm == 0:
            logger.warning("⚠️ Embedding имеет нулевую норму!")
            return embedding
        
        return embedding / norm
    
    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Cosine similarity между двумя НОРМАЛИЗОВАННЫМИ векторами
        
        similarity = dot(a, b)
        
        Результат: 0.0 (совсем разные) ... 1.0 (идентичные)
        """
        try:
            # Если векторы нормализованы, cosine_similarity = dot_product
            similarity = float(np.dot(a, b))
            
            # Убеждаемся что результат в диапазоне [0, 1]
            similarity = max(0.0, min(1.0, similarity))
            
            return similarity
        except Exception as e:
            logger.error(f"❌ Ошибка при вычислении cosine similarity: {e}")
            return 0.0
    
    def save_embedding(self, cow_id: int, face_image: np.ndarray) -> bool:
        """
        Извлекает embedding из фото и сохраняет в БД
        
        Args:
            cow_id: ID коровы
            face_image: RGB изображение морды коровы
        
        Returns:
            True если успешно, False иначе
        """
        try:
            logger.info(f"💾 Сохраняю embedding для коровы ID={cow_id}...")
            
            # Извлекаем embedding
            embedding = self.embedder.extract_embedding(face_image)
            
            if embedding is None:
                logger.error("❌ Не удалось извлечь embedding")
                return False
            
            # Находим корову
            cow = self.db.query(Cow).filter(Cow.id == cow_id).first()
            if not cow:
                logger.error(f"❌ Корова с ID {cow_id} не найдена")
                return False
            
            # Сохраняем embedding как bytes
            embedding_bytes = embedding.astype(np.float32).tobytes()
            cow.face_embedding = embedding_bytes
            
            self.db.commit()
            
            logger.info(f"✅ Embedding сохранен ({len(embedding_bytes)} bytes)")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка при сохранении embedding: {e}")
            self.db.rollback()
            return False
    
    def get_similarity_scores(self, face_image: np.ndarray, top_k: int = 5) -> List[Dict]:
        """
        Возвращает top-K коров с их similarity scores (для отладки)
        
        Args:
            face_image: RGB изображение морды
            top_k: Сколько верхних результатов вернуть
        
        Returns:
            Список [{'name': ..., 'similarity': ..., 'above_threshold': ...}, ...]
        """
        try:
            # Извлекаем embedding
            new_embedding = self.embedder.extract_embedding(face_image)
            if new_embedding is None:
                return []
            
            new_embedding_normalized = self._normalize_embedding(new_embedding)
            
            # Вычисляем similarity со всеми коровами
            similarities = []
            cows = self.db.query(Cow).filter(Cow.face_embedding.isnot(None)).all()
            
            for cow in cows:
                stored_embedding = np.frombuffer(cow.face_embedding, dtype=np.float32)
                stored_embedding_normalized = self._normalize_embedding(stored_embedding)
                similarity = self._cosine_similarity(new_embedding_normalized, stored_embedding_normalized)
                
                similarities.append({
                    'name': cow.name,
                    'similarity': similarity,
                    'above_threshold': similarity >= self.threshold
                })
            
            # Сортируем и возвращаем top-K
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:top_k]
        
        except Exception as e:
            logger.error(f"Ошибка при получении scores: {e}")
            return []


# Глобальный распознаватель
_recognizer = None


def get_recognizer(db: Session) -> CowRecognizer:
    """Получает или создает глобальный распознаватель"""
    global _recognizer
    if _recognizer is None:
        _recognizer = CowRecognizer(db)
    return _recognizer

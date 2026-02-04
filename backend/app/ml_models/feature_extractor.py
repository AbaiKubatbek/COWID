"""
Модуль для извлечения признаков лица (face embedding)
Использует pre-trained ResNet50 или FaceNet
"""
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np
from typing import Tuple
import cv2
import logging

logger = logging.getLogger(__name__)


class FaceEmbedder:
    """
    Извлекает feature embedding (вектор признаков) из морды коровы
    
    Процесс:
    1. Берём cropped изображение морды (из детектора)
    2. Нормализуем и преобразуем
    3. Пропускаем через pre-trained нейросеть (ResNet50)
    4. Получаем вектор признаков (embedding) размером 2048 или 512
    
    Этот вектор однозначно описывает морду и используется для:
    - Сравнения морд разных коров
    - Поиска по similarity в БД
    - Идентификации коровы
    """
    
    def __init__(self, embedding_size: int = 512, device: str = "cpu"):
        """
        Инициализация embedder
        
        Args:
            embedding_size: Размер output вектора (512 или 2048)
            device: "cpu" или "cuda" (для GPU)
        """
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.embedding_size = embedding_size
        
        # Используем pre-trained ResNet50
        # ResNet50 обучена на ImageNet и хорошо работает для feature extraction
        self.model = models.resnet50(pretrained=True)
        
        # Заменяем последний слой для нужного размера embedding
        # Стандартно ResNet50 возвращает 2048-мерный вектор
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, embedding_size)
        
        # Переводим в режим evaluation (без dropout и batch norm updates)
        self.model.to(self.device)
        self.model.eval()
        
        # Трансформация для входных изображений
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((224, 224)),  # ResNet требует 224x224
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],  # ImageNet mean
                std=[0.229, 0.224, 0.225]    # ImageNet std
            )
        ])
        
        logger.info(f"FaceEmbedder инициализирован на {self.device}")
    
    def extract_embedding(self, face_image: np.ndarray) -> np.ndarray:
        """
        Извлекает embedding из изображения морды
        
        Args:
            face_image: Изображение морды в формате numpy array (BGR)
        
        Returns:
            Вектор признаков размером embedding_size
        """
        try:
            # Преобразуем BGR -> RGB для PyTorch
            face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            
            # Применяем трансформации
            face_tensor = self.transform(face_image_rgb)
            
            # Добавляем batch dimension
            face_tensor = face_tensor.unsqueeze(0).to(self.device)
            
            # Извлекаем embedding (без градиентов)
            with torch.no_grad():
                embedding = self.model(face_tensor)
            
            # Нормализуем вектор (L2 norm) для лучшего сравнения
            embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)
            
            # Преобразуем в numpy array
            embedding_np = embedding.cpu().numpy().flatten()
            
            return embedding_np
        
        except Exception as e:
            logger.error(f"Ошибка при извлечении embedding: {e}")
            return np.zeros(self.embedding_size)
    
    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Вычисляет cosine similarity между двумя embedding'ами
        Значение от 0 до 1 (1 = идентичные)
        
        Args:
            embedding1: Первый вектор признаков
            embedding2: Второй вектор признаков
        
        Returns:
            Similarity score (0-1)
        """
        # Cosine similarity = (A · B) / (|A| * |B|)
        # Если embeddings нормализованы, это просто скалярное произведение
        similarity = np.dot(embedding1, embedding2)
        
        # Ограничиваем значение от 0 до 1
        similarity = max(0.0, min(1.0, similarity))
        
        return float(similarity)


# Глобальный embedder (кэшируем модель)
_embedder = None


def get_embedder(embedding_size: int = 512, device: str = "cpu") -> FaceEmbedder:
    """Singleton для получения embedder"""
    global _embedder
    if _embedder is None:
        _embedder = FaceEmbedder(embedding_size=embedding_size, device=device)
    return _embedder


# ========== АЛЬТЕРНАТИВА: FaceNet ==========
# Если хотите использовать FaceNet вместо ResNet50:
#
# from facenet_pytorch import InceptionResnetV1
#
# class FaceNetEmbedder:
#     def __init__(self, device="cpu"):
#         self.device = torch.device(device if torch.cuda.is_available() else "cpu")
#         self.model = InceptionResnetV1(pretrained='vggface2').eval().to(self.device)
#     
#     def extract_embedding(self, face_image: np.ndarray) -> np.ndarray:
#         # Преобразуем изображение
#         # Передаём в модель
#         # Получаем 512-мерный embedding
#         ...
#
# FaceNet часто даёт лучше результаты, но требует больше памяти

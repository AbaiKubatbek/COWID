"""
ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ CowID API

Этот файл содержит примеры кода для:
1. Загрузки и распознавания коровы по фото
2. Работы с API
3. Использования ML моделей
"""

# ========== ПРИМЕР 1: Распознавание по фото ==========

import requests
import cv2
from pathlib import Path

# URL backend'а
API_URL = "http://localhost:8000"

def recognize_cow_from_file(image_path: str):
    """
    Распознаёт корову по загруженному файлу
    """
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(
            f"{API_URL}/api/recognize/image",
            files=files
        )
    
    result = response.json()
    
    if result['success']:
        print(f"✅ Корова распознана: {result['cow']['name']}")
        print(f"   Уверенность: {result['confidence']:.1%}")
        print(f"   Порода: {result['cow']['breed']}")
        print(f"   Возраст: {result['cow']['age']} лет")
        if result['cow']['medical_records']:
            print(f"   Медицинские записи:")
            for record in result['cow']['medical_records']:
                print(f"     - {record['title']} ({record['record_date']})")
    else:
        print(f"⚠️ {result['message']}")
    
    return result


# Использование:
# recognize_cow_from_file("path/to/cow_photo.jpg")


# ========== ПРИМЕР 2: Управление коровами ==========

def get_all_cows():
    """Получить список всех коров"""
    response = requests.get(f"{API_URL}/api/cows")
    cows = response.json()
    
    print(f"📋 Всего коов: {len(cows)}")
    for cow in cows:
        print(f"  - {cow['name']} ({cow['breed']}, {cow['age']}л)")
    
    return cows


def create_cow_with_photo(name: str, breed: str, age: int, photo_path: str):
    """Создать новую корову с фото"""
    
    # Подготавливаем данные
    cow_data = {
        "name": name,
        "breed": breed,
        "age": age,
        "weight": 600  # опциональное поле
    }
    
    # Загружаем фото
    with open(photo_path, 'rb') as f:
        files = {'photo': f}
        data = {'cow_data': str(cow_data)}
        
        response = requests.post(
            f"{API_URL}/api/cows",
            files=files,
            data=data
        )
    
    new_cow = response.json()
    print(f"✅ Корова создана: {new_cow['name']} (ID={new_cow['id']})")
    
    return new_cow


def update_cow(cow_id: int, age: int = None, weight: float = None):
    """Обновить данные коровы"""
    
    update_data = {}
    if age is not None:
        update_data['age'] = age
    if weight is not None:
        update_data['weight'] = weight
    
    response = requests.put(
        f"{API_URL}/api/cows/{cow_id}",
        json=update_data
    )
    
    updated_cow = response.json()
    print(f"✅ Корова обновлена: {updated_cow['name']}")
    
    return updated_cow


def delete_cow(cow_id: int):
    """Удалить корову"""
    
    response = requests.delete(f"{API_URL}/api/cows/{cow_id}")
    print(f"✅ Корова удалена")


# Использование:
# get_all_cows()
# create_cow_with_photo("Bessie", "Holstein", 5, "bessie.jpg")
# update_cow(1, age=6)
# delete_cow(1)


# ========== ПРИМЕР 3: Медицинские записи ==========

def add_medical_record(cow_id: int, record_type: str, title: str, description: str):
    """Добавить медицинскую запись"""
    
    from datetime import datetime
    
    record_data = {
        "record_type": record_type,  # "vaccine", "disease", "treatment", "note"
        "title": title,
        "description": description,
        "record_date": datetime.now().isoformat()
    }
    
    response = requests.post(
        f"{API_URL}/api/cows/{cow_id}/medical-records",
        json=record_data
    )
    
    record = response.json()
    print(f"✅ Медицинская запись добавлена")
    
    return record


def get_medical_records(cow_id: int):
    """Получить все медицинские записи"""
    
    response = requests.get(f"{API_URL}/api/cows/{cow_id}/medical-records")
    records = response.json()
    
    print(f"📋 Медицинские записи для коовы {cow_id}:")
    for record in records:
        print(f"  - {record['title']} ({record['record_type']}, {record['record_date']})")
        if record['description']:
            print(f"    {record['description']}")
    
    return records


# Использование:
# add_medical_record(1, "vaccine", "Вакцина от сибирской язвы", "Плановая вакцинация")
# get_medical_records(1)


# ========== ПРИМЕР 4: Debug распознавания ==========

def recognize_with_debug(image_path: str):
    """
    Получить debug информацию о распознавании:
    - Количество обнаруженных морд
    - Top-5 совпадений
    """
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(
            f"{API_URL}/api/recognize/debug",
            files=files
        )
    
    debug_info = response.json()
    
    print(f"🔍 Debug информация:")
    print(f"   Обнаружено морд: {debug_info['detections_count']}")
    
    if debug_info['detections']:
        print(f"   Детали обнаружения:")
        for i, det in enumerate(debug_info['detections']):
            print(f"     {i+1}. Confidence: {det['confidence']:.2%}, BBox: {det['bbox']}")
    
    if debug_info.get('top_matches'):
        print(f"   Top-5 совпадений:")
        for i, match in enumerate(debug_info['top_matches']):
            print(f"     {i+1}. {match['cow_name']} (ID={match['cow_id']}, "
                  f"similarity={match['similarity']:.4f})")
    
    return debug_info


# Использование:
# recognize_with_debug("cow_photo.jpg")


# ========== ПРИМЕР 5: Работа с ML моделями напрямую ==========

import numpy as np
import cv2
from backend.app.ml_models.face_detector import get_detector
from backend.app.ml_models.feature_extractor import get_embedder
from backend.app.ml_models.face_recognizer import CowRecognizer
from backend.app.database.models import SessionLocal

def ml_pipeline_example(image_path: str):
    """
    Демонстрирует работу ML pipeline без использования HTTP API
    (полезно для тестирования и дебага)
    """
    
    # Загружаем изображение
    image = cv2.imread(image_path)
    print(f"📷 Загруженное изображение: {image.shape}")
    
    # 1. Детектируем морду
    detector = get_detector()
    detections = detector.detect_faces(image)
    print(f"🔍 Обнаружено морд: {len(detections)}")
    
    if detections:
        # Используем первую (лучшую) морду
        best_detection = detections[0]
        face_region = best_detection['face_region']
        confidence = best_detection['confidence']
        print(f"   Best detection confidence: {confidence:.2%}")
        
        # Рисуем результаты
        annotated_image = detector.draw_detections(image, detections)
        cv2.imwrite("detections.jpg", annotated_image)
        print(f"   Сохранено: detections.jpg")
        
        # 2. Извлекаем embedding
        embedder = get_embedder()
        embedding = embedder.extract_embedding(face_region)
        print(f"👤 Embedding размер: {embedding.shape}")
        print(f"   Embedding (первые 10 чисел): {embedding[:10]}")
        
        # 3. Распознаём корову
        db = SessionLocal()
        try:
            recognizer = CowRecognizer(db)
            cow_id, cow_name, similarity = recognizer.recognize(embedding)
            
            if cow_id:
                print(f"🐄 Корова распознана: {cow_name} (ID={cow_id})")
                print(f"   Similarity: {similarity:.4f}")
                
                # Получаем top-5 совпадений
                top_matches = recognizer.get_top_matches(embedding, top_k=5)
                print(f"   Top-5 совпадений:")
                for rank, (cid, cname, sim) in enumerate(top_matches, 1):
                    print(f"     {rank}. {cname} (similarity={sim:.4f})")
            else:
                print(f"⚠️ Корова не распознана (макс. similarity: {similarity:.4f})")
        finally:
            db.close()


# Использование:
# ml_pipeline_example("cow_photo.jpg")


# ========== ПРИМЕР 6: Полный workflow ==========

def full_workflow_example():
    """
    Полный пример использования системы:
    1. Создаём новую корову
    2. Добавляем медицинские записи
    3. Распознаём корову по фото
    """
    
    print("=" * 50)
    print("CowID - Полный workflow")
    print("=" * 50)
    
    # 1. Создаём новую корову
    print("\n1️⃣ Создание новой коовы...")
    # new_cow = create_cow_with_photo(
    #     "Bessie", "Holstein", 5, "bessie_photo.jpg"
    # )
    # cow_id = new_cow['id']
    
    # (для примера используем существующую корову)
    cow_id = 1
    
    # 2. Добавляем медицинские записи
    print("\n2️⃣ Добавление медицинских записей...")
    add_medical_record(cow_id, "vaccine", 
                       "Вакцина от сибирской язвы", 
                       "Плановая вакцинация")
    add_medical_record(cow_id, "note",
                       "Прибавила в весе",
                       "Увеличилась молочная продуктивность")
    
    # 3. Просматриваем все записи
    print("\n3️⃣ Просмотр медицинских записей...")
    get_medical_records(cow_id)
    
    # 4. Распознаём корову по фото
    print("\n4️⃣ Распознавание по фото...")
    # recognize_cow_from_file("test_photo.jpg")
    
    # 5. Список всех коов
    print("\n5️⃣ Список всех коов...")
    get_all_cows()
    
    print("\n" + "=" * 50)
    print("✅ Workflow завершен!")
    print("=" * 50)


# Запуск:
# full_workflow_example()


if __name__ == "__main__":
    print("CowID API - Примеры использования")
    print("Раскомментируйте нужный пример внизу")
    
    # Примеры для запуска:
    # recognize_cow_from_file("path/to/image.jpg")
    # get_all_cows()
    # ml_pipeline_example("path/to/image.jpg")
    # full_workflow_example()

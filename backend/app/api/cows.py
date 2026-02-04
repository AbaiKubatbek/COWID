"""
API маршруты для управления коровами (CRUD операции)
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from datetime import datetime
import os
import logging
from typing import List, Optional

from app.database.models import Cow, MedicalRecord, get_db
from app.schemas.cow import (
    CowCreate,
    CowUpdate,
    CowResponse,
    MedicalRecordCreate,
    MedicalRecordResponse
)
from app.ml_models.feature_extractor import get_embedder
import cv2
import numpy as np

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/cows", tags=["cows"])


# ========== CREATE ==========

@router.post("/", response_model=CowResponse)
async def create_cow(
    name: str = Form(...),
    breed: str = Form(...),
    age: int = Form(...),
    weight: Optional[float] = Form(None),
    photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Создаёт новую корову с её данными
    
    Если загружено фото:
    1. Сохраняем фото
    2. Извлекаем embedding морды
    3. Сохраняем embedding в БД
    
    Args:
        name: Имя коровы
        breed: Порода коровы
        age: Возраст коровы в годах
        weight: Вес коровы в кг
        photo: Опциональное изображение морды коровы
        db: Database session
    
    Returns:
        Созданная корова с ID
    """
    try:
        # Проверяем уникальность имени
        existing_cow = db.query(Cow).filter(Cow.name == name).first()
        if existing_cow:
            raise HTTPException(status_code=400, detail="Корова с таким именем уже существует")
        
        # Создаём новую корову
        new_cow = Cow(
            name=name,
            breed=breed,
            age=age,
            weight=weight
        )
        
        # Если загружено фото, обрабатываем его
        if photo:
            # Сохраняем фото
            photo_path = await save_upload_file(photo, name)
            new_cow.photo_path = photo_path
            
            # Извлекаем embedding морды
            image = cv2.imread(photo_path)
            if image is not None:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                embedder = get_embedder()
                embedding = embedder.extract_embedding(image_rgb)
                if embedding is not None:
                    # Сохраняем embedding как bytes
                    new_cow.face_embedding = embedding.astype(np.float32).tobytes()
        
        # Сохраняем в БД
        db.add(new_cow)
        db.commit()
        db.refresh(new_cow)
        
        logger.info(f"Создана новая корова: {new_cow.name} (ID={new_cow.id})")
        return new_cow
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при создании коовы: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ========== READ ==========

@router.get("/", response_model=List[CowResponse])
def get_all_cows(db: Session = Depends(get_db)):
    """
    Получает список всех коров
    
    Returns:
        Список всех коров с их медицинскими записями
    """
    try:
        cows = db.query(Cow).all()
        return cows
    except Exception as e:
        logger.error(f"Ошибка при получении списка коов: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cow_id}", response_model=CowResponse)
def get_cow(cow_id: int, db: Session = Depends(get_db)):
    """
    Получает информацию о конкретной корове
    
    Args:
        cow_id: ID коовы
        db: Database session
    
    Returns:
        Полные данные коовы включая медицинские записи
    """
    try:
        cow = db.query(Cow).filter(Cow.id == cow_id).first()
        if not cow:
            raise HTTPException(status_code=404, detail="Корова не найдена")
        return cow
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении коовы: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== UPDATE ==========

@router.put("/{cow_id}", response_model=CowResponse)
def update_cow(
    cow_id: int,
    cow_data: CowUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновляет данные коровы
    
    Args:
        cow_id: ID коровы
        cow_data: Новые данные (частичное обновление)
        db: Database session
    
    Returns:
        Обновлённая корова
    """
    try:
        cow = db.query(Cow).filter(Cow.id == cow_id).first()
        if not cow:
            raise HTTPException(status_code=404, detail="Корова не найдена")
        
        # Обновляем только переданные поля
        update_data = cow_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cow, field, value)
        
        cow.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(cow)
        
        logger.info(f"Корова {cow_id} обновлена")
        return cow
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обновлении коовы: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ========== DELETE ==========

@router.delete("/{cow_id}")
def delete_cow(cow_id: int, db: Session = Depends(get_db)):
    """
    Удаляет корову из системы
    
    Удаляются также все её медицинские записи (cascade delete)
    
    Args:
        cow_id: ID коровы
        db: Database session
    
    Returns:
        Подтверждение удаления
    """
    try:
        cow = db.query(Cow).filter(Cow.id == cow_id).first()
        if not cow:
            raise HTTPException(status_code=404, detail="Корова не найдена")
        
        # Удаляем фото если оно существует
        if cow.photo_path and os.path.exists(cow.photo_path):
            os.remove(cow.photo_path)
        
        # Удаляем корову (медицинские записи удаляются автоматически)
        db.delete(cow)
        db.commit()
        
        logger.info(f"Корова {cow_id} удалена")
        return {"detail": f"Корова {cow_id} удалена"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при удалении коовы: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ========== MEDICAL RECORDS ==========

@router.post("/{cow_id}/medical-records", response_model=MedicalRecordResponse)
def add_medical_record(
    cow_id: int,
    record_data: MedicalRecordCreate,
    db: Session = Depends(get_db)
):
    """
    Добавляет медицинскую запись к корове
    
    Args:
        cow_id: ID коровы
        record_data: Данные медицинской записи (вакцина, болезнь и т.д.)
        db: Database session
    
    Returns:
        Созданная медицинская запись
    """
    try:
        # Проверяем существование коровы
        cow = db.query(Cow).filter(Cow.id == cow_id).first()
        if not cow:
            raise HTTPException(status_code=404, detail="Корова не найдена")
        
        # Создаём новую медицинскую запись
        new_record = MedicalRecord(
            cow_id=cow_id,
            record_type=record_data.record_type,
            title=record_data.title,
            description=record_data.description,
            record_date=record_data.record_date
        )
        
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        logger.info(f"Добавлена медицинская запись для коровы {cow_id}")
        return new_record
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при добавлении медицинской записи: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{cow_id}/medical-records", response_model=List[MedicalRecordResponse])
def get_medical_records(cow_id: int, db: Session = Depends(get_db)):
    """
    Получает все медицинские записи коровы
    
    Args:
        cow_id: ID коровы
        db: Database session
    
    Returns:
        Список медицинских записей
    """
    try:
        cow = db.query(Cow).filter(Cow.id == cow_id).first()
        if not cow:
            raise HTTPException(status_code=404, detail="Корова не найдена")
        
        records = db.query(MedicalRecord).filter(MedicalRecord.cow_id == cow_id).all()
        return records
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении медицинских записей: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== UTILS ==========

async def save_upload_file(upload_file: UploadFile, cow_name: str) -> str:
    """
    Сохраняет загруженный файл на диск
    
    Args:
        upload_file: Загруженный файл
        cow_name: Имя коровы (для генерации имени файла)
    
    Returns:
        Путь к сохранённому файлу
    """
    from app.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
    
    # Создаём папку если её нет
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Проверяем расширение
    file_ext = upload_file.filename.split(".")[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение файла. Допустимые: {ALLOWED_EXTENSIONS}"
        )
    
    # Проверяем размер
    contents = await upload_file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Файл слишком большой")
    
    # Сохраняем файл
    filename = f"{cow_name}_{datetime.utcnow().timestamp()}.{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    return file_path

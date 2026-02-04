"""
Database configuration and models
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, LargeBinary, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

from app.config import DATABASE_URL

# Создаём engine для работы с БД
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# SessionLocal для создания сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base для всех моделей
Base = declarative_base()


# ========== MODELS ==========

class Cow(Base):
    """
    Модель коровы в БД
    """
    __tablename__ = "cows"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    breed = Column(String(255), nullable=False)  # Порода (например: "Holstein")
    age = Column(Integer, nullable=False)  # Возраст в годах
    weight = Column(Float, nullable=True)  # Вес в кг
    
    # Путь к оригинальной фотографии
    photo_path = Column(String(500), nullable=True)
    
    # Feature embedding (face embedding as bytes)
    # Это вектор признаков лица, использующийся для распознавания
    face_embedding = Column(LargeBinary, nullable=True)
    
    # Осеменение (инсеминация)
    insemination_status = Column(Boolean, default=False)  # Да/Нет
    insemination_date = Column(DateTime, nullable=True)  # Дата осеменения
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    medical_records = relationship("MedicalRecord", back_populates="cow", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cow(id={self.id}, name={self.name}, breed={self.breed})>"


class MedicalRecord(Base):
    """
    Модель медицинской карты коровы
    """
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    cow_id = Column(Integer, ForeignKey("cows.id"), nullable=False)
    
    # Тип записи: "vaccine", "disease", "treatment", "note"
    record_type = Column(String(50), nullable=False)
    
    # Название (вакцины, болезни, и т.д.)
    title = Column(String(255), nullable=False)
    
    # Описание
    description = Column(Text, nullable=True)
    
    # Дата события
    record_date = Column(DateTime, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    cow = relationship("Cow", back_populates="medical_records")

    def __repr__(self):
        return f"<MedicalRecord(id={self.id}, cow_id={self.cow_id}, type={self.record_type})>"


# Создаём все таблицы
Base.metadata.create_all(bind=engine)


# ========== DEPENDENCY INJECTION ==========

def get_db():
    """
    Dependency для получения сессии БД
    Используется в маршрутах FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

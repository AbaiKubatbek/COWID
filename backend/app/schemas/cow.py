"""
Pydantic schemas для валидации данных
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# ========== COW SCHEMAS ==========

class MedicalRecordCreate(BaseModel):
    """Схема для создания медицинской записи"""
    record_type: str  # "vaccine", "disease", "treatment", "note"
    title: str
    description: Optional[str] = None
    record_date: datetime


class MedicalRecordResponse(BaseModel):
    """Схема ответа медицинской записи"""
    id: int
    cow_id: int
    record_type: str
    title: str
    description: Optional[str] = None
    record_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CowCreate(BaseModel):
    """Схема для создания коровы"""
    name: str
    breed: str
    age: int
    weight: Optional[float] = None
    insemination_status: Optional[bool] = False
    insemination_date: Optional[datetime] = None


class CowUpdate(BaseModel):
    """Схема для обновления коровы"""
    name: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    insemination_status: Optional[bool] = None
    insemination_date: Optional[datetime] = None


class CowResponse(BaseModel):
    """Полный ответ с данными коровы"""
    id: int
    name: str
    breed: str
    age: int
    weight: Optional[float] = None
    photo_path: Optional[str] = None
    insemination_status: Optional[bool] = False
    insemination_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    medical_records: List[MedicalRecordResponse] = []

    class Config:
        from_attributes = True


# ========== RECOGNITION SCHEMAS ==========

class RecognitionResult(BaseModel):
    """Результат распознавания коровы"""
    success: bool
    cow_id: Optional[int] = None
    cow_name: Optional[str] = None
    confidence: float  # 0.0 - 1.0
    message: str


class RecognitionWithDetails(BaseModel):
    """Результат распознавания с полной информацией о корове"""
    success: bool
    cow: Optional[CowResponse] = None
    confidence: float
    message: str

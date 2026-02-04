# CowID Backend

## 📋 Описание

FastAPI backend для системы распознавания лиц коров. Обрабатывает компьютерное зрение, машинное обучение и управление данными коов.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Создаём виртуальное окружение
python -m venv venv

# Активируем (Windows)
venv\Scripts\activate

# Активируем (Linux/Mac)
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
python -m uvicorn app.main:app --reload
```

Приложение будет доступно на `http://localhost:8000`

API документация (Swagger UI): `http://localhost:8000/docs`

## 📁 Структура проекта

```
app/
├── main.py                    # Главный файл FastAPI
├── config.py                  # Конфигурация
├── api/
│   ├── cows.py               # CRUD для коов
│   └── recognize.py          # Распознавание (image + video stream)
├── ml_models/
│   ├── face_detector.py      # YOLOv8 детектор морд
│   ├── feature_extractor.py  # ResNet50 для embedding
│   └── face_recognizer.py    # Распознавание по embedding
├── database/
│   └── models.py             # SQLAlchemy ORM модели
└── schemas/
    └── cow.py                # Pydantic валидация
```

## 🔌 API Endpoints

### Управление коровами (CRUD)

#### GET /api/cows
Получить список всех коов
```json
Response: [
  {
    "id": 1,
    "name": "Bessie",
    "breed": "Holstein",
    "age": 5,
    "weight": 600,
    "photo_path": "uploads/Bessie_123456.jpg",
    "created_at": "2024-01-15T10:30:00",
    "medical_records": [...]
  }
]
```

#### POST /api/cows
Создать новую корову с фото
```bash
curl -X POST http://localhost:8000/api/cows \
  -F "cow_data={\"name\":\"Bessie\",\"breed\":\"Holstein\",\"age\":5,\"weight\":600}" \
  -F "photo=@cow_photo.jpg"
```

#### GET /api/cows/{cow_id}
Получить информацию о конкретной корове

#### PUT /api/cows/{cow_id}
Обновить данные коовы

#### DELETE /api/cows/{cow_id}
Удалить корову

#### POST /api/cows/{cow_id}/medical-records
Добавить медицинскую запись

#### GET /api/cows/{cow_id}/medical-records
Получить медицинские записи

### Распознавание

#### POST /api/recognize/image
Распознать корову по загруженному фото
```bash
curl -X POST http://localhost:8000/api/recognize/image \
  -F "image=@cow_photo.jpg"
```

Response:
```json
{
  "success": true,
  "cow": {
    "id": 1,
    "name": "Bessie",
    "breed": "Holstein",
    "age": 5,
    "medical_records": [...]
  },
  "confidence": 0.95,
  "message": "Корова успешно распознана: Bessie"
}
```

#### POST /api/recognize/debug
Debug версия с top-5 совпадениями

#### WS /api/recognize/stream
WebSocket для видеопотока в реальном времени

## 🧠 ML Pipeline

### 1. Детекция морды (YOLOv8)
- Входит: Исходное изображение
- Выходит: Bounding box морды коовы
- Модель: YOLOv8 nano (предобученная)

### 2. Извлечение признаков (ResNet50)
- Входит: Cropped изображение морды
- Выходит: 512-мерный embedding (вектор признаков)
- Модель: ResNet50 (предобученная на ImageNet)
- Нормализация: L2 norm

### 3. Распознавание (Similarity Matching)
- Входит: Embedding новой морды
- Процесс: Сравнение cosine similarity с embeddings в БД
- Выходит: ID коовы если similarity > threshold (0.6)

## 💾 База данных

### Таблица Cows
| Поле | Тип | Описание |
|------|-----|---------|
| id | Integer | Первичный ключ |
| name | String | Имя коовы |
| breed | String | Порода |
| age | Integer | Возраст |
| weight | Float | Вес (кг) |
| photo_path | String | Путь к фото |
| face_embedding | LargeBinary | Вектор признаков |
| created_at | DateTime | Дата создания |

### Таблица MedicalRecords
| Поле | Тип | Описание |
|------|-----|---------|
| id | Integer | Первичный ключ |
| cow_id | Integer | ID коовы (FK) |
| record_type | String | Тип: vaccine/disease/treatment/note |
| title | String | Название |
| description | Text | Описание |
| record_date | DateTime | Дата события |

## 🔧 Конфигурация

Отредактируйте `app/config.py`:

```python
# База данных
DATABASE_URL = "sqlite:///./cows.db"  # SQLite для dev
# DATABASE_URL = "postgresql://user:pass@localhost/cowid"  # PostgreSQL для prod

# Confidence thresholds
DETECTION_CONFIDENCE = 0.5      # Для детекции морды
RECOGNITION_CONFIDENCE = 0.6    # Для распознавания
```

Или используйте `.env` файл:
```
DATABASE_URL=postgresql://user:password@localhost/cowid_db
RECOGNITION_CONFIDENCE=0.65
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## 🚀 Production Deploy

### Docker

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t cowid-backend .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... cowid-backend
```

### Docker Compose

```yaml
version: '3'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://postgres:password@db:5432/cowid
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: cowid
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## 📊 Мониторинг

Доступные endpoints:
- `/docs` - Swagger UI
- `/redoc` - ReDoc документация
- `/openapi.json` - OpenAPI schema
- `/health` - Health check
- `/` - Информация об API

## 🐛 Дебаг

Для дебага используйте:
```bash
# Debug endpoint с top-5 совпадениями
curl -X POST http://localhost:8000/api/recognize/debug \
  -F "image=@cow_photo.jpg"
```

## 📝 Логирование

Логи пишутся в консоль и содержат:
- Время события
- Уровень (INFO, WARNING, ERROR)
- Имя модуля
- Сообщение

Пример:
```
2024-01-15 10:30:45 - app.ml_models.face_detector - INFO - Модель детекции загружена
2024-01-15 10:31:00 - app.api.recognize - INFO - Корова распознана: Bessie (similarity: 0.9534)
```

## ⚙️ Performance

- Детекция морды: ~200ms (GPU: ~50ms)
- Извлечение embedding: ~100ms (GPU: ~20ms)
- Распознавание: ~10ms (в-памяти поиск)
- Всего на 1 фото: ~300ms (GPU: ~80ms)

Для видеопотока обрабатываем каждый 3-й фрейм (10 FPS вместо 30) для лучшей производительности.

## 🤝 Вклад

Если у вас есть идеи улучшений:
1. Используйте custom-trained YOLOv8 для морд коров (даст улучшение на 20-30%)
2. Экспериментируйте с ArcFace или CosFace для лучшего embedding
3. Добавьте кэширование embeddings в Redis
4. Реализуйте batch processing для массовой загрузки коов

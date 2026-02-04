# CowID - Система распознавания лиц коров

## 📋 Архитектура проекта

### Общее описание
CowID - веб-приложение для распознавания и идентификации коров на основе компьютерного зрения и глубокого обучения.

## 🏗️ Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Admin Panel  │  │ Recognition  │  │ Medical Card│       │
│  │   (CRUD)     │  │   (Image)    │  │  (Profile)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              ↓
                        HTTP REST API
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ API Routes (Routers)                                 │   │
│  │  - /api/cows (CRUD)                                 │   │
│  │  - /api/recognize (Image Upload)                    │   │
│  │  - /api/recognize/stream (WebSocket - Video)        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ ML/CV Pipeline                                       │   │
│  │  - Face Detection (YOLOv8)                           │   │
│  │  - Face Recognition (FaceNet/ResNet)                │   │
│  │  - Feature Extraction                               │   │
│  │  - Similarity Matching                              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Database Models (SQLAlchemy)                         │   │
│  │  - Cow (ID, Name, Breed, Age, Photo)               │   │
│  │  - MedicalRecord (Vaccines, Diseases, Notes)        │   │
│  │  - FaceEmbedding (Feature vectors)                  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Database (SQLite/PostgreSQL)                    │
│  - Cows table                                               │
│  - Medical records                                          │
│  - Face embeddings (для быстрого поиска)                   │
└─────────────────────────────────────────────────────────────┘
```

## 💾 Стек технологий

### Backend
- **FastAPI** - современный веб-фреймворк
- **Python 3.9+** - язык программирования
- **SQLAlchemy** - ORM для работы с БД
- **PostgreSQL/SQLite** - база данных
- **OpenCV** - обработка изображений
- **PyTorch/TensorFlow** - глубокое обучение
- **YOLOv8** - детекция объектов (морда коровы)
- **FaceNet/ResNet50** - извлечение признаков лица
- **Pillow** - работа с изображениями
- **numpy, scipy** - численные вычисления

### Frontend
- **React 18+** - UI фреймворк
- **Vite/Create React App** - сборщик
- **Axios** - HTTP клиент
- **TailwindCSS** - стили
- **Zustand/Redux** - state management
- **Webcam.js** - доступ к камере

## 🗂️ Структура проекта

```
CowID/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Главный файл приложения
│   │   ├── config.py               # Конфигурация
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── cows.py             # CRUD операции коров
│   │   │   └── recognize.py        # Распознавание лиц
│   │   ├── ml_models/
│   │   │   ├── __init__.py
│   │   │   ├── face_detector.py    # YOLOv8 детектор
│   │   │   ├── face_recognizer.py  # Распознавание
│   │   │   ├── feature_extractor.py# Извлечение признаков
│   │   │   └── weights/            # Предобученные веса
│   │   ├── database/
│   │   │   ├── __init__.py
│   │   │   ├── db.py               # Подключение к БД
│   │   │   └── models.py           # ORM модели
│   │   └── schemas/
│   │       ├── __init__.py
│   │       └── cow.py              # Pydantic схемы
│   ├── requirements.txt
│   ├── .env
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AdminPanel.jsx      # Admin интерфейс
│   │   │   ├── CowList.jsx         # Список коров
│   │   │   ├── RecognitionForm.jsx # Загрузка изображения
│   │   │   ├── VideoCapture.jsx    # Видеопоток
│   │   │   └── MedicalCard.jsx     # Карточка коровы
│   │   ├── pages/
│   │   │   ├── AdminPage.jsx
│   │   │   ├── RecognitionPage.jsx
│   │   │   └── HomePage.jsx
│   │   ├── services/
│   │   │   └── api.js              # API клиент
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── ARCHITECTURE.md
└── README.md
```

## 🔄 Flow процессов

### Распознавание по изображению
1. Пользователь загружает изображение → Frontend отправляет на Backend
2. Backend: OpenCV + YOLOv8 → Детекция морды коровы
3. Backend: Извлечение feature vector (embedding) морды
4. Backend: Поиск по similarity в базе embeddings
5. Backend: Возвращает ID коровы и confidence score
6. Frontend: Отображает медицинскую карту коровы

### Распознавание в реальном времени
1. Frontend: Захват видеопотока с камеры
2. Frontend → Backend: Отправка фреймов (30 fps)
3. Backend: Обработка каждого фрейма (обычно каждый Nth фрейм)
4. Backend: Отправка результатов через WebSocket
5. Frontend: Отображение результата + медицинской карты

### Admin панель (CRUD)
1. Create: Фермер добавляет новую корову + фото
2. Backend: Обработка фото, извлечение embedding, сохранение в БД
3. Read: Просмотр списка всех коров
4. Update: Редактирование данных (имя, возраст, болезни и т.д.)
5. Delete: Удаление коровы из системы

## 🔐 Аутентификация и безопасность

- Простая аутентификация (логин/пароль для админа)
- Токены (JWT) для API
- HTTPS в production
- Валидация входных данных (Pydantic)
- CORS для frontend

## 📊 База данных

### Таблица Cows
- id (PK)
- name
- breed
- age
- photo_path
- face_embedding (BLOB - вектор признаков)
- created_at
- updated_at

### Таблица MedicalRecords
- id (PK)
- cow_id (FK)
- vaccine_name
- disease_name
- notes
- date
- created_at

## 🚀 Развертывание

### Development
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Production
- Docker контейнеры
- Docker Compose для оркестрации
- Nginx как reverse proxy
- PostgreSQL вместо SQLite
- Gunicorn для Backend
- Nginx для Frontend

## 📝 API Endpoints

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/api/cows` | Получить всех коров |
| POST | `/api/cows` | Создать новую корову |
| GET | `/api/cows/{cow_id}` | Получить данные коровы |
| PUT | `/api/cows/{cow_id}` | Обновить коову |
| DELETE | `/api/cows/{cow_id}` | Удалить корову |
| POST | `/api/recognize` | Распознать корову по фото |
| WS | `/api/recognize/stream` | WebSocket для видеопотока |


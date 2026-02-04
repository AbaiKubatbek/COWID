# 📋 Полная структура проекта CowID

```
CowID/
│
├─ 📚 ДОКУМЕНТАЦИЯ
│  ├─ README.md                    ⭐ Главная документация проекта
│  ├─ ARCHITECTURE.md              Подробная архитектура системы
│  ├─ INSTALL.md                   Пошаговое руководство установки
│  ├─ PROJECT_SUMMARY.md           Краткое резюме проекта
│  ├─ EXAMPLES.py                  Примеры использования API
│  └─ .gitignore                   Git конфигурация
│
├─ 🐳 DOCKER & DEPLOYMENT
│  ├─ docker-compose.yml           Docker Compose для запуска всего
│  ├─ start.sh                     Быстрый старт скрипт (Linux/Mac)
│  └─ backend/Dockerfile           Dockerfile для Backend
│     frontend/Dockerfile          Dockerfile для Frontend
│
├─ 🔙 BACKEND (FastAPI + Python)
│  │
│  ├─ app/
│  │  ├─ __init__.py              
│  │  ├─ main.py                  ⭐ FastAPI приложение (entry point)
│  │  ├─ config.py                ⭐ Конфигурация (DB, ML params)
│  │  │
│  │  ├─ api/
│  │  │  ├─ __init__.py
│  │  │  ├─ cows.py               ⭐ CRUD маршруты (создание, чтение, обновление, удаление)
│  │  │  │  - POST /api/cows
│  │  │  │  - GET /api/cows
│  │  │  │  - GET /api/cows/{id}
│  │  │  │  - PUT /api/cows/{id}
│  │  │  │  - DELETE /api/cows/{id}
│  │  │  │  - POST /api/cows/{id}/medical-records
│  │  │  │  - GET /api/cows/{id}/medical-records
│  │  │  │
│  │  │  └─ recognize.py          ⭐ Маршруты распознавания
│  │  │     - POST /api/recognize/image (распознавание по фото)
│  │  │     - POST /api/recognize/debug (debug инфо)
│  │  │     - WS /api/recognize/stream (видеопоток WebSocket)
│  │  │
│  │  ├─ ml_models/
│  │  │  ├─ __init__.py
│  │  │  ├─ face_detector.py       ⭐ YOLOv8 - детекция морды коровы
│  │  │  │  класс FaceDetector:
│  │  │  │  - detect_faces(image) -> List[detection]
│  │  │  │  - draw_detections(image, detections) -> annotated_image
│  │  │  │
│  │  │  ├─ feature_extractor.py  ⭐ ResNet50 - извлечение признаков (embedding)
│  │  │  │  класс FaceEmbedder:
│  │  │  │  - extract_embedding(face_image) -> np.array (512-мерный вектор)
│  │  │  │  - compute_similarity(emb1, emb2) -> float (0-1)
│  │  │  │
│  │  │  └─ face_recognizer.py    ⭐ Распознавание по embeddings
│  │  │     класс CowRecognizer:
│  │  │     - recognize(embedding) -> (cow_id, cow_name, confidence)
│  │  │     - get_top_matches(embedding, top_k=5) -> List[match]
│  │  │     - update_embedding(cow_id, embedding) -> bool
│  │  │
│  │  ├─ database/
│  │  │  ├─ __init__.py
│  │  │  └─ models.py             ⭐ SQLAlchemy ORM модели
│  │  │     - class Cow (имя, порода, возраст, вес, фото, embedding)
│  │  │     - class MedicalRecord (вакцины, болезни, заметки)
│  │  │     - SessionLocal для работы с БД
│  │  │     - get_db() dependency injection
│  │  │
│  │  └─ schemas/
│  │     ├─ __init__.py
│  │     └─ cow.py                ⭐ Pydantic схемы для валидации
│  │        - CowCreate (для создания)
│  │        - CowUpdate (для обновления)
│  │        - CowResponse (для ответа)
│  │        - MedicalRecordCreate
│  │        - MedicalRecordResponse
│  │        - RecognitionResult
│  │        - RecognitionWithDetails
│  │
│  ├─ requirements.txt             ⭐ Python зависимости
│  │  ├─ FastAPI, Uvicorn
│  │  ├─ SQLAlchemy (ORM)
│  │  ├─ PyTorch, OpenCV
│  │  ├─ Ultralytics (YOLOv8)
│  │  ├─ Pydantic (валидация)
│  │  └─ ... (полный список)
│  │
│  ├─ .env.example                 ⭐ Пример конфигурации
│  │
│  ├─ Dockerfile                   Docker образ для Backend
│  │
│  └─ README.md                    Backend документация
│
├─ 🎨 FRONTEND (React + Vite)
│  │
│  ├─ src/
│  │  ├─ main.jsx                 Entry point для React
│  │  │
│  │  ├─ App.jsx                  ⭐ Главный компонент приложения
│  │  │  - Navigation (выбор страницы)
│  │  │  - Маршрутизация: Home, Recognition, Admin
│  │  │  - Footer
│  │  │
│  │  ├─ index.css                Tailwind CSS стили + кастомные
│  │  │
│  │  ├─ components/
│  │  │  ├─ AdminPanel.jsx        ⭐ Admin панель (CRUD)
│  │  │  │  - Список коов
│  │  │  │  - Форма добавления новой коовы
│  │  │  │  - Форма редактирования
│  │  │  │  - Управление медицинскими записями
│  │  │  │  - Удаление коов
│  │  │  │
│  │  │  ├─ RecognitionForm.jsx   ⭐ Распознавание по фото
│  │  │  │  - Загрузка файла
│  │  │  │  - Preview изображения
│  │  │  │  - Вызов API распознавания
│  │  │  │  - Отображение результатов
│  │  │  │
│  │  │  ├─ MedicalCard.jsx       ⭐ Медицинская карта коровы
│  │  │  │  - Основная информация (имя, порода, возраст)
│  │  │  │  - Фото коровы
│  │  │  │  - История медицинских записей
│  │  │  │  - Форматирование данных
│  │  │  │
│  │  │  └─ VideoCapture.jsx      (не включен в основную версию)
│  │  │     Будущий компонент для видеопотока в реальном времени
│  │  │
│  │  ├─ services/
│  │  │  └─ api.js                ⭐ API клиент (Axios)
│  │  │     - getCows()
│  │  │     - getCow(id)
│  │  │     - createCow(data, photo)
│  │  │     - updateCow(id, data)
│  │  │     - deleteCow(id)
│  │  │     - getMedicalRecords(id)
│  │  │     - addMedicalRecord(id, data)
│  │  │     - recognizeFromImage(file)
│  │  │     - recognizeWithDebug(file)
│  │  │     - connectVideoStream(onMessage)
│  │  │
│  │  └─ store/
│  │     └─ store.js              ⭐ Zustand state management
│  │        - useCowStore (управление коовами)
│  │        - useRecognitionStore (результаты распознавания)
│  │        - useUIStore (состояние интерфейса)
│  │
│  ├─ index.html                  ⭐ HTML шаблон
│  │
│  ├─ package.json                ⭐ NPM зависимости
│  │  ├─ React 18
│  │  ├─ Vite
│  │  ├─ Tailwind CSS
│  │  ├─ Axios
│  │  ├─ Zustand
│  │  └─ React Router
│  │
│  ├─ vite.config.js              Vite конфигурация (HMR, proxy)
│  │
│  ├─ Dockerfile                  Docker образ для Frontend
│  │
│  └─ README.md                   Frontend документация
│
└─ 🔧 КОНФИГУРАЦИЯ
   ├─ docker-compose.yml          Оркестрация всех сервисов
   └─ .gitignore                  Игнорирование файлов в Git
```

---

## 📊 Связь между компонентами

```
┌────────────────────────────┐
│   Frontend (React/Vite)    │
│  - App.jsx (маршрутизация) │
│  - AdminPanel.jsx (CRUD)   │
│  - RecognitionForm.jsx     │
│  - MedicalCard.jsx         │
└────────────────┬───────────┘
                 │ Axios HTTP
                 │ WebSocket
                 ▼
┌────────────────────────────┐
│   Backend (FastAPI)        │
│  - main.py (приложение)    │
│  - api/cows.py (CRUD)      │
│  - api/recognize.py        │
└────────────────┬───────────┘
                 │ SQLAlchemy
                 ▼
┌────────────────────────────┐
│  Database (SQLite/PG)      │
│  - Cows таблица            │
│  - MedicalRecords таблица  │
└────────────────────────────┘
                 ▲
                 │ Вызовы ML
┌────────────────┴───────────┐
│   ML Pipeline              │
│  1. YOLOv8 (face_detector) │
│  2. ResNet50 (embedder)    │
│  3. Similarity (recognizer)│
└────────────────────────────┘
```

---

## 🔄 Типичные потоки данных

### Создание новой коровы
```
Frontend (AdminPanel)
  ↓ (POST /api/cows + фото)
Backend (cows.py)
  ↓ Сохранение фото
Backend (face_detector.py)
  ↓ Детекция морды
Backend (feature_extractor.py)
  ↓ Извлечение embedding
Database (models.py)
  ↓ Сохранение в Cows таблицу
Frontend (AdminPanel)
  ↓ Обновление списка
```

### Распознавание по фото
```
Frontend (RecognitionForm)
  ↓ (POST /api/recognize/image + фото)
Backend (recognize.py)
  ↓ Загрузка изображения
Backend (face_detector.py)
  ↓ Детекция морды
Backend (feature_extractor.py)
  ↓ Извлечение embedding
Backend (face_recognizer.py)
  ↓ Cosine similarity поиск в БД
Database (models.py)
  ↓ Получение данных коовы
Frontend (MedicalCard)
  ↓ Отображение результата
```

---

## 🎯 Ключевые файлы для изучения

### Обязательно прочитать
1. **[README.md](./README.md)** - Общее описание проекта
2. **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Архитектура и дизайн
3. **[INSTALL.md](./INSTALL.md)** - Установка и запуск

### Backend код
1. **[backend/app/main.py](./backend/app/main.py)** - FastAPI приложение
2. **[backend/app/api/cows.py](./backend/app/api/cows.py)** - CRUD операции
3. **[backend/app/api/recognize.py](./backend/app/api/recognize.py)** - Распознавание
4. **[backend/app/ml_models/face_detector.py](./backend/app/ml_models/face_detector.py)** - YOLOv8 детектор
5. **[backend/app/ml_models/feature_extractor.py](./backend/app/ml_models/feature_extractor.py)** - ResNet50
6. **[backend/app/database/models.py](./backend/app/database/models.py)** - ORM модели

### Frontend код
1. **[frontend/src/App.jsx](./frontend/src/App.jsx)** - Главный компонент
2. **[frontend/src/components/AdminPanel.jsx](./frontend/src/components/AdminPanel.jsx)** - Admin панель
3. **[frontend/src/components/RecognitionForm.jsx](./frontend/src/components/RecognitionForm.jsx)** - Распознавание
4. **[frontend/src/services/api.js](./frontend/src/services/api.js)** - API клиент
5. **[frontend/src/store/store.js](./frontend/src/store/store.js)** - Zustand store

### Примеры
- **[EXAMPLES.py](./EXAMPLES.py)** - Примеры использования API

---

## 📦 Зависимости и версии

### Backend
- Python 3.9+
- FastAPI 0.104+
- SQLAlchemy 2.0+
- PyTorch 2.1+
- OpenCV 4.8+
- Ultralytics YOLOv8 8.0+

### Frontend
- Node.js 16+
- React 18+
- Vite 5+
- Tailwind CSS 3.3+
- Axios 1.6+
- Zustand 4.4+

### Database
- SQLite (development)
- PostgreSQL 12+ (production)

---

## 🚀 Быстрые команды

```bash
# Docker (рекомендуется)
docker-compose up

# Локально - Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Локально - Frontend
cd frontend
npm install
npm run dev

# Production build
npm run build
docker build -t cowid-backend ./backend
docker build -t cowid-frontend ./frontend
```

---

## 📞 Помощь и поддержка

- **Прочитайте [INSTALL.md](./INSTALL.md)** для пошагового руководства
- **Смотрите [EXAMPLES.py](./EXAMPLES.py)** для примеров кода
- **Проверьте Backend документацию** в [backend/README.md](./backend/README.md)
- **Проверьте Frontend документацию** в [frontend/README.md](./frontend/README.md)
- **API документация** на http://localhost:8000/docs (Swagger UI)

---

**CowID v1.0** - Полнофункциональная система распознавания лиц коров на основе ИИ

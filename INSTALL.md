# CowID - Полное руководство по установке и использованию

## 📦 Содержание

1. [Требования](#требования)
2. [Быстрый старт](#быстрый-старт)
3. [Установка компонентов](#установка-компонентов)
4. [Запуск приложения](#запуск-приложения)
5. [Использование](#использование)
6. [Troubleshooting](#troubleshooting)

---

## Требования

- **Python 3.9+** - для backend'а
- **Node.js 16+** - для frontend'а
- **PostgreSQL 12+** (или SQLite для development)
- **Git** - для управления версиями
- **GPU (рекомендуется)** - NVIDIA CUDA для ускорения ML моделей

## Быстрый старт

### 1 строка для запуска с Docker

```bash
docker-compose up
```

Затем откройте:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Установка компонентов

### Вариант 1: Локальная установка

#### Backend

```bash
# Перейти в папку
cd backend

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
copy .env.example .env
# или отредактировать вручную

# Запустить backend
python -m uvicorn app.main:app --reload
```

Backend будет на: http://localhost:8000
Документация: http://localhost:8000/docs

#### Frontend

```bash
# Перейти в папку
cd frontend

# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
```

Frontend будет на: http://localhost:3000

### Вариант 2: Docker

```bash
# Build и запуск
docker-compose up --build

# В фоне
docker-compose up -d

# Остановка
docker-compose down
```

---

## Запуск приложения

### Development

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Production

```bash
# Backend с Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app.main:app

# Frontend build и serve
npm run build
npm install -g serve
serve -s dist -l 3000
```

### Docker Production

```bash
# Собрать с production флагом
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

---

## Использование

### Первый запуск

1. **Откройте Frontend**: http://localhost:3000
2. **Перейдите в Admin**: нажмите "⚙️ Admin" в меню
3. **Добавьте корову**:
   - Нажмите "+ Добавить"
   - Заполните имя, породу, возраст
   - Загрузите фото морды коровы
   - Сохраните

4. **Распознайте корову**:
   - Перейдите в "🔍 Распознавание"
   - Загрузите фото
   - Нажмите "🔍 Распознать"
   - Увидите медицинскую карту

### API использование

#### cURL примеры

```bash
# Получить всех коов
curl http://localhost:8000/api/cows

# Распознать по фото
curl -X POST http://localhost:8000/api/recognize/image \
  -F "image=@cow_photo.jpg"

# Создать новую корову
curl -X POST http://localhost:8000/api/cows \
  -F 'cow_data={"name":"Bessie","breed":"Holstein","age":5,"weight":600}' \
  -F "photo=@photo.jpg"
```

#### Python примеры

```python
import requests

# Распознать корову
response = requests.post(
    'http://localhost:8000/api/recognize/image',
    files={'image': open('cow.jpg', 'rb')}
)
result = response.json()
print(f"Распознана: {result['cow']['name']}")
```

### ML Pipeline использование

```python
from app.ml_models.face_detector import get_detector
from app.ml_models.feature_extractor import get_embedder
from app.ml_models.face_recognizer import CowRecognizer
import cv2

# Загружаем изображение
image = cv2.imread('cow.jpg')

# 1. Детекция
detector = get_detector()
detections = detector.detect_faces(image)

if detections:
    face = detections[0]['face_region']
    
    # 2. Extraction
    embedder = get_embedder()
    embedding = embedder.extract_embedding(face)
    
    # 3. Recognition
    from app.database.models import SessionLocal
    db = SessionLocal()
    recognizer = CowRecognizer(db)
    cow_id, cow_name, confidence = recognizer.recognize(embedding)
    
    print(f"Коова: {cow_name}, confidence: {confidence:.2%}")
```

---

## Структура базы данных

### Таблица Cows

| Поле | Тип | Описание |
|------|-----|---------|
| id | int | Первичный ключ |
| name | str | Имя коовы (уникальное) |
| breed | str | Порода |
| age | int | Возраст в годах |
| weight | float | Вес в кг |
| photo_path | str | Путь к фото |
| face_embedding | blob | Feature vector (512 чисел) |
| created_at | datetime | Дата создания |
| updated_at | datetime | Дата обновления |

### Таблица MedicalRecords

| Поле | Тип | Описание |
|------|-----|---------|
| id | int | Первичный ключ |
| cow_id | int | ID коовы (FK) |
| record_type | str | Тип: vaccine/disease/treatment/note |
| title | str | Название |
| description | str | Описание |
| record_date | datetime | Дата события |
| created_at | datetime | Дата создания |
| updated_at | datetime | Дата обновления |

---

## Конфигурация

### Backend конфиг (.env)

```
# Database
DATABASE_URL=sqlite:///./cows.db
# или для PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/cowid_db

# ML Settings
DETECTION_CONFIDENCE=0.5          # Порог детекции морды
RECOGNITION_CONFIDENCE=0.6        # Порог распознавания

# Security
SECRET_KEY=your-secret-key
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# Server
HOST=0.0.0.0
PORT=8000
```

### Frontend конфиг (.env)

```
VITE_API_URL=http://localhost:8000/api
```

---

## Performance

| Операция | CPU | GPU |
|----------|-----|-----|
| Детекция морды (YOLOv8) | 200ms | 50ms |
| Извлечение embedding (ResNet50) | 100ms | 20ms |
| Поиск в БД (100 коов) | 10ms | 10ms |
| **Всего на фото** | **310ms** | **80ms** |
| **Видеопоток (10 FPS)** | **~100ms** | **~30ms** |

---

## Troubleshooting

### Backend не запускается

```bash
# Проверить Python версию
python --version  # Должно быть 3.9+

# Проверить зависимости
pip list

# Переустановить requirements
pip install -r requirements.txt --force-reinstall

# Проверить порт
netstat -ano | findstr :8000
```

### CUDA/GPU не работает

```bash
# Проверить CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Если False - используется CPU автоматически
# Для явного использования CPU:
# Отредактируйте app/config.py и установите DEVICE="cpu"
```

### Database ошибка

```bash
# Для SQLite - удалить и пересоздать
rm cows.db

# Для PostgreSQL - проверить подключение
psql -U username -d cowid_db -c "SELECT 1"
```

### Frontend ошибка подключения к backend

```bash
# Проверить CORS в backend (должно быть в config.py)
ALLOWED_ORIGINS = ["http://localhost:3000"]

# Проверить что backend запущен
curl http://localhost:8000/health

# Проверить переменную окружения в .env
VITE_API_URL=http://localhost:8000/api
```

### Медленная обработка

1. **Используйте GPU**: установите CUDA + torch GPU версию
2. **Уменьшите размер модели**: используйте YOLOv8n вместо YOLOv8s
3. **Кэшируйте результаты**: добавьте Redis для кэша embeddings
4. **Batch processing**: обрабатывайте множество фото одновременно

---

## Обновление и развертывание

### Production checklist

- [ ] Изменить SECRET_KEY на случайное значение
- [ ] Использовать PostgreSQL вместо SQLite
- [ ] Включить HTTPS (SSL сертификат)
- [ ] Настроить CORS для продакшена
- [ ] Добавить rate limiting
- [ ] Настроить логирование
- [ ] Добавить мониторинг (prometheus/grafana)
- [ ] Настроить резервное копирование БД
- [ ] Включить аутентификацию для API

### Обновление кода

```bash
# Обновить backend
cd backend
git pull origin main
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Обновить frontend
cd frontend
git pull origin main
npm install
npm run build
```

---

## Логирование

### Backend логи

```bash
# Real-time логи
tail -f app.log

# Все логи
cat app.log | grep ERROR
```

### Frontend логи

Смотрите Developer Console (F12 -> Console tab)

---

## Дополнительные ресурсы

- [FastAPI документация](https://fastapi.tiangolo.com/)
- [React документация](https://react.dev/)
- [YOLOv8 документация](https://docs.ultralytics.com/models/yolov8/)
- [PyTorch документация](https://pytorch.org/docs/)

---

## Поддержка

При возникновении проблем:

1. Проверьте [Troubleshooting](#troubleshooting) раздел выше
2. Посмотрите логи backend'а
3. Проверьте Developer Console в browser'е (F12)
4. Прочитайте README в папке backend/ и frontend/

---

## Лицензия

MIT License

---

<div align="center">
  <p>CowID v1.0 - Система распознавания лиц коров</p>
  <p>Сделано с ❤️ для животноводства</p>
</div>

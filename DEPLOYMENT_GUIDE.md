# 🚀 CowID - Полное руководство по развёртыванию

## Оглавление
1. [Быстрый старт](#быстрый-старт-локально)
2. [Развёртывание на Vercel (Frontend)](#развёртывание-frontend-на-vercel)
3. [Развёртывание на Render (Backend)](#развёртывание-backend-на-render)
4. [Развёртывание с Docker](#развёртывание-с-docker-docker-compose)
5. [Переменные окружения](#переменные-окружения)
6. [Тестирование](#тестирование)

---

## Быстрый старт (Локально)

### Требования
- Python 3.8+
- Node.js 16+
- Git

### Установка и запуск

```bash
# 1. Клонируем проект
git clone <repo-url>
cd CowID

# 2. Установка Backend зависимостей
cd backend
pip install -r requirements.txt
cd ..

# 3. Установка Frontend зависимостей  
cd frontend
npm install
cd ..

# 4. Запуск Backend (терминал 1)
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. Запуск Frontend (терминал 2)
cd frontend
npm run dev

# 6. Открываем браузер
# Frontend: http://localhost:5173
# Backend Swagger: http://localhost:8000/docs
```

---

## Развёртывание Frontend на Vercel

### Шаг 1: Подготовка

```bash
# 1. Зайти на https://vercel.com и создать аккаунт
# 2. Подключить GitHub репозиторий

# 3. В корне проекта создаём vercel.json (если не существует)
```

### Шаг 2: Конфигурация Vercel

Frontend уже имеет `vercel.json` в папке frontend/. Проверьте, что там:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist"
}
```

### Шаг 3: Переменные окружения в Vercel

В панели Vercel добавьте переменные:

```
VITE_API_URL=https://cowid-backend-production.onrender.com/api
```

### Шаг 4: Deploy

```bash
# Вариант 1: Через Vercel CLI
npm install -g vercel
cd frontend
vercel --prod

# Вариант 2: Автоматический через GitHub
# Просто сделайте git push - Vercel автоматически деплойнет
```

**Результат**: Frontend будет доступен на `https://<your-project>.vercel.app`

---

## Развёртывание Backend на Render

### Шаг 1: Подготовка репозитория

Backend уже имеет `render.yaml`. Проверьте содержимое:

```yaml
services:
  - type: web
    name: cowid-backend
    runtime: python
    pythonVersion: 3.11
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHONUNBUFFERED
        value: true
      - key: DATABASE_URL
        value: sqlite:///./cows.db
```

### Шаг 2: Deploy на Render

1. Зайти на https://render.com
2. Создать аккаунт и подключить GitHub
3. Нажать "New +" → "Web Service"
4. Выбрать репозиторий CowID
5. Заполнить:
   - **Name**: `cowid-backend`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Branch**: `main`

### Шаг 3: Переменные окружения

В Render добавьте:

```
RECOGNITION_CONFIDENCE=0.55
DETECTION_CONFIDENCE=0.5
DATABASE_URL=postgresql://...  (если используете PostgreSQL)
```

### Шаг 4: Deploy

Нажмите "Create Web Service" и ждите развёртывания (~5-10 минут).

**Результат**: Backend будет доступен на `https://cowid-backend.onrender.com`

---

## Развёртывание с Docker (Docker Compose)

### Шаг 1: Docker Compose файл

Проект имеет `docker-compose.yml`. Проверьте его структуру.

### Шаг 2: Сборка образов

```bash
# Сборка обоих контейнеров
docker-compose build

# Запуск
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### Шаг 3: Доступ

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Backend Swagger: http://localhost:8000/docs

### Остановка

```bash
docker-compose down
```

---

## Переменные окружения

### Backend (.env файл)

```env
# Database
DATABASE_URL=sqlite:///./cows.db
# или для PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost:5432/cowid_db

# Security
SECRET_KEY=your-secret-key-change-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

# ML Models
DETECTION_CONFIDENCE=0.5
RECOGNITION_CONFIDENCE=0.55

# CORS
ALLOWED_ORIGINS=http://localhost:5173,https://yourdomain.vercel.app
```

### Frontend (.env файл)

```env
VITE_API_URL=http://localhost:8000/api
# Для production:
# VITE_API_URL=https://cowid-backend.onrender.com/api
```

---

## Тестирование

### Локальное тестирование

```bash
# 1. Backend тесты
cd backend
pytest

# 2. Frontend тесты
cd ../frontend
npm run test
```

### Production чек-лист

- [ ] Backend запущен на Render и доступен
- [ ] Frontend запущен на Vercel и доступен
- [ ] Кросс-доменные запросы работают (CORS правильный)
- [ ] Переменные окружения установлены
- [ ] БД инициализирована (проверить через /api/cows)
- [ ] Камера работает в браузере
- [ ] Распознавание работает
- [ ] Админ панель работает

### Тестирование API

```bash
# Проверить, что backend работает
curl https://cowid-backend.onrender.com/docs

# Создать корову (тестовые данные)
curl -X POST https://cowid-backend.onrender.com/api/cows \
  -F "name=Bessie" \
  -F "breed=Holstein" \
  -F "age=5"

# Получить список коров
curl https://cowid-backend.onrender.com/api/cows

# Проверить здоровье
curl https://cowid-backend.onrender.com/health
```

---

## Troubleshooting

### Frontend не подключается к Backend

**Проблема**: CORS ошибка в браузере

**Решение**:
1. Проверить переменные окружения (VITE_API_URL)
2. Проверить CORS в backend/app/main.py
3. Убедиться, что URLs правильные

### Backend медленно загружается

**Проблема**: Первая загрузка моделей (~2-3 минуты)

**Решение**: Это нормально при первом запуске (загрузка YOLOv8 и ResNet50)

### Камера не работает

**Проблема**: "Permission denied" при открытии камеры

**Решение**:
1. Убедиться, что сайт на HTTPS (requirement для getUserMedia)
2. Позволить доступ к камере в браузере
3. На мобильных - открыть через HTTPS

### БД ошибки

**Проблема**: "no such column" при создании коровы

**Решение**:
```bash
# Удалить старую БД и пересоздать
cd backend
rm cows.db
python -m uvicorn app.main:app --reload
```

---

## Дополнительно

### Оптимизация для Production

1. **Backend**:
   - Использовать PostgreSQL вместо SQLite
   - Включить GPU (если доступно)
   - Кэшировать embeddings в Redis
   - Настроить логирование

2. **Frontend**:
   - Включить сжатие (gzip)
   - Минификация CSS/JS
   - Оптимизация изображений
   - Service Worker для offline режима

3. **DevOps**:
   - Настроить CI/CD (GitHub Actions)
   - Мониторинг и алерты
   - Автоматические тесты
   - Резервные копии БД

### Контакты поддержки

- Documentation: [README.md](README.md)
- Issues: GitHub Issues
- Email: support@cowid.local

---

**Последнее обновление**: 2026-02-04  
**Версия**: 1.0.0  
**Статус**: ✅ Production-Ready

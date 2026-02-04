# TERMINAL COMMANDS - Все команды для деплоя в одном месте

## 🔵 BACKEND SETUP

### Запустить backend сервер
```bash
cd C:\Users\user\Desktop\CowID\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Очистить БД
```bash
Remove-Item cows.db -Force -ErrorAction SilentlyContinue
```

### Проверить что backend запущен
```bash
# Открыть в браузере: http://localhost:8000/docs
# Должна открыться Swagger UI
```

---

## 🔵 FRONTEND SETUP

### Установить зависимости
```bash
cd C:\Users\user\Desktop\CowID\frontend
npm install
```

### Запустить dev сервер
```bash
cd C:\Users\user\Desktop\CowID\frontend
npm run dev
# Результат: http://localhost:5173
```

### Создать production build
```bash
cd C:\Users\user\Desktop\CowID\frontend
npm run build
# Результат: папка dist/ создана
```

### Preview production build
```bash
cd C:\Users\user\Desktop\CowID\frontend
npm run preview
# Результат: http://localhost:4173
```

---

## 🟢 VERCEL DEPLOYMENT

### Установить Vercel CLI
```bash
npm install -g vercel
```

### Проверить версию Vercel CLI
```bash
vercel --version
```

### Логин в Vercel (первый раз)
```bash
vercel login
# Откроется браузер для авторизации
```

### Развернуть на production
```bash
cd C:\Users\user\Desktop\CowID\frontend
vercel --prod
# Результат: https://cowid-frontend.vercel.app
```

### Развернуть на preview (для тестирования)
```bash
cd C:\Users\user\Desktop\CowID\frontend
vercel
# Результат: https://cowid-preview-abc123.vercel.app
```

### Проверить статус деплоя
```bash
vercel list
```

### Удалить проект с Vercel
```bash
vercel remove cowid-frontend
```

---

## 🟣 DEVELOPMENT WORKFLOWS

### Полный цикл: Backend + Frontend (локально)

**Терминал 1 - Backend:**
```bash
cd C:\Users\user\Desktop\CowID\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Терминал 2 - Frontend:**
```bash
cd C:\Users\user\Desktop\CowID\frontend
npm run dev
```

**Результат:**
- Backend: http://0.0.0.0:8000
- Frontend: http://localhost:5173
- Документация API: http://localhost:8000/docs

---

### Production Deployment (все шаги)

```bash
# 1. Backend production
cd C:\Users\user\Desktop\CowID\backend
Remove-Item cows.db -Force
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 2. Frontend build
cd C:\Users\user\Desktop\CowID\frontend
npm run build

# 3. Deploy to Vercel
vercel --prod

# 4. Получить URL и открыть на мобильном
# https://cowid-frontend.vercel.app
```

---

## 🟠 GIT COMMANDS (если используешь GitHub)

### Инициализировать git репо
```bash
cd C:\Users\user\Desktop\CowID\frontend
git init
git add .
git commit -m "Initial commit: CowID React app"
```

### Добавить GitHub репо
```bash
git remote add origin https://github.com/твой-юзер/cowid-frontend.git
git branch -M main
git push -u origin main
```

### Push изменений
```bash
git add .
git commit -m "Описание изменений"
git push
```

### Клонировать репо
```bash
git clone https://github.com/твой-юзер/cowid-frontend.git
cd cowid-frontend
npm install
```

---

## 🟡 TROUBLESHOOTING COMMANDS

### Очистить npm кэш
```bash
npm cache clean --force
```

### Удалить node_modules и переустановить
```bash
cd C:\Users\user\Desktop\CowID\frontend
Remove-Item node_modules -Recurse -Force
npm install
```

### Проверить версии
```bash
node --version
npm --version
vercel --version
```

### Проверить что слушает порт 8000
```bash
# Windows
netstat -ano | findstr :8000

# Если процесс там - убить его
taskkill /PID <PID> /F
```

### Проверить что слушает порт 5173
```bash
netstat -ano | findstr :5173
```

---

## 📊 ЛОГИРОВАНИЕ И ОТЛАДКА

### Посмотреть логи backend
```bash
# Если backend запущен с --reload, логи видны в терминале
# Ошибки будут выделены красным цветом
```

### Посмотреть логи frontend (консоль браузера)
```bash
# F12 → Console tab
# Там будут логи с тегами [CameraComponent], [API], и т.д.
```

### Посмотреть логи Vercel деплоя
```bash
vercel logs cowid-frontend
```

---

## ✅ ПРИМЕРЫ ПОЛНЫХ СЦЕНАРИЕВ

### Сценарий 1: Быстрый локальный тест (2 мин)
```bash
# Терминал 1
cd backend && python -m uvicorn app.main:app --reload

# Терминал 2
cd frontend && npm run dev

# Браузер: http://localhost:5173
```

### Сценарий 2: Production на Vercel (5 мин)
```bash
cd frontend
npm run build
vercel login
vercel --prod
# Готово на: https://cowid-frontend.vercel.app
```

### Сценарий 3: GitHub + Vercel автоматический деплой
```bash
# 1. Push на GitHub
git push

# 2. Vercel автоматически начнет деплой
# 3. Через 2-3 минуты приложение обновится

# Посмотреть статус:
vercel list
vercel logs cowid-frontend
```

---

**Версия:** 1.0.0  
**Дата:** 2026-02-04

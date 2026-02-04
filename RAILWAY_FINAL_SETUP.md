# ✅ RAILWAY DEPLOYMENT - Пошаговая инструкция

## 🎯 В Railway Dashboard сделать:

### 1. Добавить переменные окружения

В Railway перейти: **Settings** → **Variables**

Добавить:
```
RECOGNITION_CONFIDENCE=0.70
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://cowidentity.netlify.app
```

### 2. Убедиться в конфигурации build

Railway должен показывать:
```
Root directory: backend/ (или пусто если backend в корне)
Build command: (оставить пусто или auto)
Start command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 3. Запустить деплой

1. Нажать **"Deploy"** в Railway Dashboard
2. Или сделать `git push` в репо - Railway автоматически задеплоит

### 4. Получить URL

После деплоя Railway покажет URL типа:
```
https://cowid-api.up.railway.app
```

## 🔗 Добавить в Netlify

1. Перейти: https://app.netlify.com/projects/cowidentity
2. **Site settings** → **Build & deploy** → **Environment**
3. Добавить переменную:
   ```
   VITE_API_URL = https://ТВОЙ-RAILWAY-URL/api
   ```
4. Нажать **"Trigger deploy"**

## ✅ Готово!

Теперь фронтенд будет подключаться к backend'у на Railway.

---

**Если что-то не работает:**
- Проверить CORS в Railway logs
- Убедиться что VITE_API_URL правильный
- Проверить что backend здоров: `https://твой-url/docs`

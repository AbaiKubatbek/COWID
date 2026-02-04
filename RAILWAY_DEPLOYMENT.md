# 🚀 Развертывание Backend на Railway (бесплатно!)

## Шаг 1: Подготовка GitHub репозитория

```bash
# Если еще не git репо:
cd C:\Users\user\Desktop\CowID
git init

# Добавить backend
git add backend/
git commit -m "Add backend"

# Создать репо на GitHub и push
git branch -M main
git remote add origin https://github.com/ТВОй_ЮЗЕР/CowID.git
git push -u origin main
```

## Шаг 2: Деплой на Railway

1. **Перейти на** [railway.app](https://railway.app)
2. **Нажать** "Start a New Project"
3. **Выбрать** "Deploy from GitHub"
4. **Залогиниться** с GitHub
5. **Выбрать** репозиторий `CowID`
6. **В настройках выбрать:**
   - Root directory: `backend/`
   - Service name: `cowid-api`

## Шаг 3: Переменные окружения

На странице проекта Railway добавить:

```
RECOGNITION_CONFIDENCE=0.70
CORS_ORIGINS=https://cowidentity.netlify.app
```

## Шаг 4: Получить URL

После деплоя Railway даст URL типа:
```
https://railway.app/project/xxxx
```

Нужна ссылка на API в формате:
```
https://cowid-api.up.railway.app/api
```

(Точный URL будет видно в Railway Dashboard)

## Шаг 5: Добавить в Netlify

На Netlify (https://app.netlify.com/projects/cowidentity):

1. **Site settings** → **Build & deploy** → **Environment**
2. **Edit variables**
3. Добавить:
   ```
   VITE_API_URL = https://cowid-api.up.railway.app/api
   ```
4. **Trigger redeploy**

---

**Готово! 🎉**

Frontend + Backend полностью развернуты на облаке с HTTPS!

# 🚀 Деплой CowID на Vercel с камерой на мобильных

## 📋 ПОЛНАЯ ИНСТРУКЦИЯ ДЕПЛОЯ

### Шаг 1: Подготовка локально

```bash
# 1.1 Перейти в папку frontend
cd C:\Users\user\Desktop\CowID\frontend

# 1.2 Установить зависимости (если не установлены)
npm install

# 1.3 Создать production build
npm run build

# 1.4 Проверить что build создан
ls dist/   # Должны быть index.html, assets/ и т.д.
```

### Шаг 2: Установить Vercel CLI

```bash
# Глобальная установка
npm install -g vercel

# Проверить установку
vercel --version
```

### Шаг 3: Логин в Vercel

```bash
# Первый раз - запросит логин через браузер
vercel login

# Выбрать способ логина:
# - GitHub (рекомендуется)
# - GitLab
# - Email
```

### Шаг 4: Деплой на Vercel

```bash
# Из папки frontend
cd C:\Users\user\Desktop\CowID\frontend

# Production деплой
vercel --prod

# ИЛИ staging (для тестирования)
vercel
```

**Vercel спросит:**
```
? Set up and deploy "frontend"? (y/N) → y
? Which scope do you want to deploy to? → (выбрать свой)
? Link to existing project? → n (первый раз)
? Project name? → cowid-frontend
? Directory? → . (текущий)
```

### Шаг 5: Проверить в браузере

```
✓ Production: https://cowid-frontend.vercel.app
```

---

## 🔧 КОНФИГУРАЦИЯ VERCEL.JSON

**vercel.json** уже обновлен! Вот что там:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Что это делает:**
- ✅ `buildCommand`: запускает `npm run build` (Vite)
- ✅ `outputDirectory`: ищет готовый проект в `dist/`
- ✅ `routes`: все маршруты → `index.html` (SPA работает!)
- ✅ Vercel автоматически раздает HTTPS сертификат

---

## 📱 ПРОВЕРКА КАМЕРЫ НА МОБИЛЬНОМ

### Требования:

1. **HTTPS** - обязательно (медиа API требует безопасности)
2. **Разрешение от юзера** - браузер спросит доступ к камере
3. **Mobil Chrome/Safari** - поддерживают `navigator.mediaDevices.getUserMedia`

### Пошагово на телефоне:

**1. Открыть ссылку на телефоне:**
```
https://cowid-frontend.vercel.app
```

**2. Нажать на кнопку "📷 Открыть камеру"** (или "Camera")

**3. Браузер спросит разрешение:**
```
"CowID хочет получить доступ к камере"
→ Нажать "Разрешить"
```

**4. Если камера работает:**
- ✅ Видно видеопоток с камеры
- ✅ Можно снять фото
- ✅ Система распознает корову

**5. Если НЕ работает, проверить:**
- ❌ Не HTTPS → не будет работать
- ❌ Юзер отказал доступ → нужно разрешить в настройках
- ❌ На iOS Safari → может требовать iOS 14.5+
- ❌ На Android Chrome → обновить браузер

---

## 💻 КОД ДОСТУПА К КАМЕРЕ

Вот минимальный пример (уже в CameraModal.jsx):

```javascript
// Запрос доступа к камере
async function startCamera() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "environment", // Задняя камера (по умолчанию)
        // или: facingMode: "user"  // Передняя камера
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    });

    // Вывести видеопоток на video element
    const video = document.getElementById('video');
    video.srcObject = stream;
    video.play();

    return stream;
  } catch (error) {
    console.error('❌ Ошибка доступа к камере:', error);
    
    if (error.name === 'NotAllowedError') {
      alert('❌ Вы запретили доступ к камере');
    } else if (error.name === 'NotFoundError') {
      alert('❌ Камера не найдена на устройстве');
    } else if (error.name === 'NotSecureError') {
      alert('❌ Требуется HTTPS для доступа к камере!');
    }
  }
}
```

### Требования:

```javascript
navigator.mediaDevices.getUserMedia({
  video: {
    facingMode: "environment",  // задняя камера на телефоне
    width: { ideal: 1280 },     // разрешение
    height: { ideal: 720 }
  },
  audio: false                  // без микрофона
})
```

---

## ⚙️ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ

На Vercel добавить переменные для backend API:

### В Vercel Dashboard:

1. Перейти на https://vercel.com → твой проект
2. **Settings** → **Environment Variables**
3. Добавить:

```
VITE_API_URL = https://cowid-backend.onrender.com/api
```

4. Пересоздать деплой:
```bash
vercel --prod
```

---

## ✅ ФИНАЛЬНЫЙ ЧЕКЛИСТ

- [ ] `npm run build` работает без ошибок
- [ ] `dist/` содержит `index.html`
- [ ] `vercel.json` обновлен с SPA routes
- [ ] Деплой через `vercel --prod` успешен
- [ ] Ссылка доступна по HTTPS
- [ ] На мобильном: камера работает
- [ ] На мобильном: можно снять фото и распознать корову

---

## 🔄 ОБНОВЛЕНИЕ ПОСЛЕ ИЗМЕНЕНИЙ

Если внесли изменения в код:

```bash
# 1. Новый build
npm run build

# 2. Деплой обновления
vercel --prod

# Готово! Изменения будут live за ~30 сек
```

---

## 🆘 РЕШЕНИЕ ТИПИЧНЫХ ПРОБЛЕМ

### Проблема: "Камера не работает"

```
✓ Решение 1: Открыть через HTTPS (на Vercel автоматически)
✓ Решение 2: Дать разрешение браузеру на доступ
✓ Решение 3: Перезагрузить страницу (F5)
✓ Решение 4: Обновить мобильный браузер
```

### Проблема: "Маршруты не работают (404 на refresh)"

```
✓ Решение: Убедиться что vercel.json содержит SPA routes
```

### Проблема: "API возвращает CORS ошибку"

```
✓ Решение: Backend должен быть на отдельном домене (Render)
✓ И иметь CORS headers правильно настроены
```

### Проблема: "Старая версия кэшируется"

```bash
# Очистить кэш Vercel
vercel --prod --force

# Или в браузере: Ctrl+Shift+Del
```

---

## 🎯 РЕЗУЛЬТАТ

Когда всё готово:

```
✅ Frontend: https://cowid-frontend.vercel.app
✅ Backend: https://cowid-backend.onrender.com
✅ Камера на мобильном: РАБОТАЕТ 📷
✅ Распознавание коров: РАБОТАЕТ 🐄
```

---

**Версия:** 1.0.0  
**Дата:** 2026-02-04  
**Статус:** ✅ Production-Ready

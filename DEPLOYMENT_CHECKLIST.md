# ✅ DEPLOYMENT CHECKLIST - Финальный чеклист перед деплоем

## 📋 ФАЗ 1: Подготовка (30 минут)

### 1.1 Проверить backend

```bash
# Перейти в папку backend
cd C:\Users\user\Desktop\CowID\backend

# ✅ Проверить что все файлы на месте
ls -la app/ml_models/
# Должны быть:
# - face_recognizer.py (НОВЫЙ)
# - feature_extractor.py
# - face_detector.py

# ✅ Проверить что config.py обновлен
# RECOGNITION_CONFIDENCE должно быть 0.70
type app\config.py | findstr RECOGNITION_CONFIDENCE

# ✅ Проверить что recognize.py обновлен
# Должна быть строка: from app.ml_models.face_recognizer import get_recognizer
type app\api\recognize.py | findstr get_recognizer

# ✅ Проверить что cows.py обновлен
# Должна быть строка: embedder.extract_embedding()
type app\api\cows.py | findstr extract_embedding
```

**Результат:** ✅ Все файлы обновлены

---

### 1.2 Проверить frontend

```bash
# Перейти в папку frontend
cd C:\Users\user\Desktop\CowID\frontend

# ✅ Проверить vercel.json
type vercel.json | findstr "buildCommand"
# Должно быть: "buildCommand": "npm run build"

# ✅ Проверить package.json
type package.json | findstr "vite"
# Должно быть наличие Vite в зависимостях

# ✅ Проверить что CameraComponent.jsx создан
ls -la src\components\CameraComponent.jsx

# ✅ Проверить что cameraUtils.js обновлен
type src\utils\cameraUtils.js | findstr "getCameraInfo"
```

**Результат:** ✅ Все конфиги на месте

---

### 1.3 Установить зависимости

```bash
# Frontend
cd C:\Users\user\Desktop\CowID\frontend
npm install

# Backend (опционально, если меняли requirements.txt)
cd C:\Users\user\Desktop\CowID\backend
pip install -r requirements.txt
```

**Результат:** ✅ Все зависимости установлены

---

## 📋 ФАЗ 2: Локальное тестирование (20 минут)

### 2.1 Тест backend на локальном

```bash
# ВАЖНО: Очистить старую БД
cd C:\Users\user\Desktop\CowID\backend
Remove-Item cows.db -Force

# Запустить сервер
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Результат должен быть:
# Uvicorn running on http://0.0.0.0:8000
# Quit the server with CTRL+C

# ✅ Проверить что API доступен
# Открыть в браузере: http://localhost:8000/docs
# Должна открыться Swagger UI документация
```

**Результат:** ✅ Backend запущен и доступен

---

### 2.2 Тест frontend на локальном

```bash
# В новом терминале
cd C:\Users\user\Desktop\CowID\frontend
npm run dev

# Результат:
#   VITE v5.0.0 ready in 123 ms
#   ➜  Local:   http://localhost:5173/
```

**Результат:** ✅ Frontend запущен

---

### 2.3 Тест на браузере

1. Открыть http://localhost:5173 в браузере
2. ✅ Видна главная страница приложения
3. ✅ Кнопка "📷 Открыть камеру" видна
4. ✅ Консоль (F12) не показывает ошибок
5. **На desktop браузере** (не на мобильном):
   - Нажать "Открыть камеру"
   - ✅ Браузер спросит разрешение на камеру
   - ✅ Камера откроется (если есть на компьютере)
   - ✅ Можно снять фото
   - ✅ Можно отправить на распознавание

**Результат:** ✅ Локальное тестирование успешно

---

## 📋 ФАЗ 3: Production Build (15 минут)

### 3.1 Создать production build

```bash
cd C:\Users\user\Desktop\CowID\frontend

# Очистить старый build (опционально)
Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue

# Создать production build
npm run build

# Результат должен быть:
# vite v5.0.0 building for production...
# dist/index.html 10.5 kb
# dist/assets/App-abc123.js 50.2 kb
# ✓ built in 2.5s

# ✅ Проверить что папка dist создана
ls -la dist\
# Должны быть файлы:
# - index.html
# - assets/
```

**Результат:** ✅ Production build создан в папке `dist/`

---

### 3.2 Локальный preview production build

```bash
# Preview production build (опционально)
npm run preview

# Результат:
#   ➜  Local:   http://localhost:4173/

# ✅ Открыть в браузере и проверить что все работает
```

**Результат:** ✅ Production build работает локально

---

## 📋 ФАЗ 4: Vercel Deployment (10 минут)

### 4.1 Установить Vercel CLI

```bash
# Проверить что Vercel CLI установлен
vercel --version

# Если нет - установить
npm install -g vercel

# Проверить еще раз
vercel --version
```

**Результат:** ✅ Vercel CLI установлен

---

### 4.2 Логин в Vercel

```bash
# Первый раз - войти в аккаунт
vercel login

# Откроется браузер, авторизуйся:
# - GitHub
# - GitLab
# - Bitbucket
# - Email

# В терминале появится: ✓ Success! Logged in as your@email.com

# Проверить что токен сохранен
type $env:USERPROFILE\.vercel\auth.json 2>$null
# Если ошибка - авторизация еще не завершена
```

**Результат:** ✅ Авторизирован в Vercel

---

### 4.3 Развернуть проект

```bash
# Перейти в папку frontend (где находится vercel.json)
cd C:\Users\user\Desktop\CowID\frontend

# Развернуть production версию
# ⚠️ ВАЖНО: --prod означает production deployment (не preview!)
vercel --prod

# Интерактивные вопросы:
# ? Set up and deploy "~/CowID/frontend"? [y/N] y
# ? Which scope do you want to deploy to? [account-name] [Enter]
# ? Link to existing project? [y/N] n
# ? What's your project's name? cowid-frontend
# ? In which directory is your code located? ./ [Enter]
# ? Auto-detect build command and settings? [Y/n] y

# Результат:
# ✓ Linked to your-account/cowid-frontend
# ✓ Inspect: https://vercel.com/your-account/cowid-frontend/abc123xyz
# ✓ Production: https://cowid-frontend.vercel.app

# 📌 СОХРАНЯЙ ЭТУ ССЫЛКУ! Это твой production URL
```

**Результат:** ✅ Проект развернут на Vercel

---

## 📋 ФАЗ 5: Проверка Production (10 минут)

### 5.1 Проверить что приложение доступно

```bash
# Открыть ссылку в браузере
https://cowid-frontend.vercel.app

# ✅ Проверить:
# - Страница загружается
# - Видна главная страница
# - Нет ошибок в консоли (F12)
# - Ссылка HTTPS (замочек 🔒 в адресной строке)
```

**Результат:** ✅ Production версия доступна

---

### 5.2 Проверить что камера работает на desktop браузере

```
1. Открыть https://cowid-frontend.vercel.app (production)
2. Нажать "📷 Открыть камеру"
3. ✅ Браузер спросит разрешение на камеру
4. ✅ Дать разрешение
5. ✅ Видно видеопоток с камеры
6. ✅ Нажать "✅ Снять фото"
7. ✅ Фото захвачено
8. ✅ Нажать "🚀 Отправить"
9. ✅ Система отправила на backend и получила результат
```

**Результат:** ✅ Камера и API интеграция работают

---

## 📋 ФАЗ 6: Мобильное тестирование (15 минут)

### 6.1 Подготовить URL

```
Ссылка для мобильного:
https://cowid-frontend.vercel.app

✅ Убедиться что:
- Ссылка HTTPS (обязательно!)
- Ссылка доступна (можешь открыть с компьютера)
- Интернет работает
```

**Результат:** ✅ URL готов

---

### 6.2 Открыть на мобильном iPhone

```
На iPhone:
1. Открыть Safari браузер
2. В адресной строке вставить: https://cowid-frontend.vercel.app
3. Нажать "Go"

✅ Проверить:
- Страница загружается
- Видна главная страница приложения
- Кнопка "📷 Открыть камеру" видна
- ✅ Нажать кнопку "📷 Открыть камеру"

4. Safari спросит разрешение:
   "Allow this website to access your camera?"
   
5. Нажать "Allow" (или "Allow Once")

✅ Проверить:
- ✅ Видно видеопоток с камеры iPhone (задняя камера)
- ✅ Можно двигать телефон и видеть изменения
- ✅ Нажать "✅ Снять фото"
- ✅ Фото захвачено
- ✅ Нажать "🚀 Отправить"
- ✅ Система отправила фото и показала результат распознавания

Если все ✅ - iOS работает!
```

**Результат:** ✅ iOS (iPhone/iPad) работает

---

### 6.3 Открыть на мобильном Android

```
На Android:
1. Открыть Chrome браузер (или Firefox)
2. В адресной строке вставить: https://cowid-frontend.vercel.app
3. Нажать "Go"

✅ Проверить:
- Страница загружается
- Видна главная страница приложения
- Кнопка "📷 Открыть камеру" видна
- ✅ Нажать кнопку "📷 Открыть камеру"

4. Chrome спросит разрешение на камеру:
   - Появится окно с кнопками "Allow" / "Don't Allow"
   
5. Нажать "Allow"

✅ Проверить:
- ✅ Видно видеопоток с камеры телефона (задняя камера)
- ✅ Можно двигать телефон и видеть изменения
- ✅ Нажать "✅ Снять фото"
- ✅ Фото захвачено
- ✅ Нажать "🚀 Отправить"
- ✅ Система отправила фото и показала результат распознавания

Если все ✅ - Android работает!
```

**Результат:** ✅ Android работает

---

## ⚠️ ВОЗМОЖНЫЕ ПРОБЛЕМЫ

### ❌ Камера не работает на мобильном

**Проверить по порядку:**

1. **HTTPS?** (Обязательно!)
   ```
   ✓ https://cowid-frontend.vercel.app (ПРАВИЛЬНО)
   ✗ http://localhost:5173 (НЕПРАВИЛЬНО)
   ```

2. **Браузер спросил разрешение?**
   - iOS: Settings → Safari → Camera → ON
   - Android: Settings → Apps → Chrome → Permissions → Camera → Allow

3. **Другое приложение не использует камеру?**
   - Закрыть: WhatsApp, Telegram, Zoom, другие видео-приложения

4. **Браузер поддерживает?**
   - ✓ Chrome (Android)
   - ✓ Safari (iOS 12.2+)
   - ✓ Firefox
   - ✗ IE11 (не поддерживает)

---

### ❌ "Security Error"

```
Причина: Требуется HTTPS

Решение:
- Использовать Vercel (автоматически HTTPS)
- Не использовать http:// на мобильном
```

---

### ❌ "NotAllowedError"

```
Причина: Браузер запросил разрешение, но ты отказал

Решение:
- iOS: Settings → Safari → Camera → Allow
- Android: Settings → Apps → Chrome → Permissions → Camera
- Перезагрузить браузер
```

---

## ✅ ФИНАЛЬНЫЙ ЧЕКЛИСТ

```
BACKEND:
- [ ] face_recognizer.py обновлен (embeddings + cosine similarity)
- [ ] config.py имеет RECOGNITION_CONFIDENCE = 0.70
- [ ] recognize.py обновлен (используется get_recognizer)
- [ ] cows.py обновлен (используется embedder.extract_embedding)
- [ ] Backend запущен локально и доступен на http://localhost:8000

FRONTEND BUILD:
- [ ] npm run build успешно завершен
- [ ] Папка dist/ создана и содержит index.html
- [ ] vercel.json правильный (buildCommand, outputDirectory, routes)
- [ ] CameraComponent.jsx создан и скопирован в src/components/

VERCEL DEPLOYMENT:
- [ ] vercel CLI установлен
- [ ] Логин в Vercel успешен (vercel login)
- [ ] vercel --prod успешно завершен
- [ ] Production URL получен: https://cowid-frontend.vercel.app

PRODUCTION TESTING:
- [ ] Production URL открывается в браузере
- [ ] Видна главная страница приложения
- [ ] Кнопка камеры видна
- [ ] На desktop: камера работает
- [ ] На iPhone: камера работает
- [ ] На Android: камера работает
- [ ] Распознавание работает (отправка фото на backend)

ИТОГ:
- [ ] ✅ ВСЕ ГОТОВО - ПРИЛОЖЕНИЕ ПОЛНОСТЬЮ РАЗВЕРНУТО
```

---

## 🎯 ИТОГОВЫЙ РЕЗУЛЬТАТ

Если все пункты чеклиста ✅:

```
✅ Frontend развернут на Vercel с HTTPS
✅ Камера работает на мобильных устройствах (iOS и Android)
✅ Фото отправляется на backend
✅ Backend распознает коров через embeddings + cosine similarity
✅ Результаты отображаются пользователю

🎉 ПОЛНОЕ ПРИЛОЖЕНИЕ ГОТОВО К ИСПОЛЬЗОВАНИЮ!
```

---

**Версия:** 1.0.0  
**Дата:** 2026-02-04  
**Время на выполнение:** ~90 минут  
**Сложность:** Средняя (требует внимания к деталям)

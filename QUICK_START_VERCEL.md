# 🚀 QUICK START - Быстрый старт (5 минут)

## Если ты в спешке

### ШАГИ (только необходимое):

#### 1️⃣ Backend (1 мин)

```bash
cd C:\Users\user\Desktop\CowID\backend

# Удалить старую БД
Remove-Item cows.db -Force -ErrorAction SilentlyContinue

# Запустить
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Результат:** `http://0.0.0.0:8000` доступен

---

#### 2️⃣ Frontend Build (2 мин)

```bash
cd C:\Users\user\Desktop\CowID\frontend

# Собрать
npm run build

# Результат: папка dist/ создана
```

✅ **Результат:** `dist/` готов к деплою

---

#### 3️⃣ Vercel Deploy (2 мин)

```bash
cd C:\Users\user\Desktop\CowID\frontend

# Если первый раз
vercel login

# Развернуть
vercel --prod

# Результат: https://cowid-frontend.vercel.app (или твой URL)
```

✅ **Результат:** Приложение на Vercel с HTTPS

---

## 📱 На мобильном

```
1. Открыть: https://cowid-frontend.vercel.app
2. Нажать: "📷 Открыть камеру"
3. Разрешить доступ к камере
4. Снять фото коровы
5. Нажать: "🚀 Отправить"
6. Готово! ✅
```

---

## ❌ Если камера не работает

```
Проверить:
1. HTTPS? (не http://)
2. Разрешение браузера? (Settings → Camera)
3. Другое приложение не использует камеру?
```

💡 **Подробнее:** смотри TROUBLESHOOTING.md или DEPLOYMENT_CHECKLIST.md

---

**Вот и всё! 🎉**

Приложение готово к использованию на мобильном с камерой.

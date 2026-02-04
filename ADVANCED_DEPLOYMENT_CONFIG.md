# 🚀 ADVANCED DEPLOYMENT CONFIG ДЛЯ VERCEL

## 📋 Содержание

1. [vercel.json - Полная конфигурация](#vercel-json)
2. [Пример React компонента с камерой](#react-компонент)
3. [Пошаговый деплой](#пошаговый-деплой)
4. [Мобильное тестирование](#мобильное-тестирование)
5. [Troubleshooting](#troubleshooting)

---

## vercel.json

### Конфигурация для Vite + SPA

```json
{
  "projectName": "cowid",
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "installCommand": "npm install",
  "framework": "vite",
  "nodeVersion": "18.x",
  
  "env": {
    "VITE_API_URL": "@vite_api_url"
  },
  
  "envPrefix": "VITE_",
  
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-backend-api.com/api/$1",
      "headers": {
        "Access-Control-Allow-Origin": "*"
      }
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  
  "headers": [
    {
      "source": "/dist/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/index.html",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, must-revalidate"
        }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Credentials",
          "value": "true"
        },
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        },
        {
          "key": "Access-Control-Allow-Methods",
          "value": "GET,OPTIONS,PATCH,DELETE,POST,PUT"
        },
        {
          "key": "Access-Control-Allow-Headers",
          "value": "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
        }
      ]
    }
  ],
  
  "regions": ["iad1"]
}
```

### Объяснение основных параметров:

| Параметр | Значение | Описание |
|----------|----------|----------|
| `buildCommand` | `npm run build` | Vite команда для сборки |
| `outputDirectory` | `dist` | Папка где лежит собранный код (для Vite) |
| `framework` | `vite` | Используем Vite, а не CRA |
| `nodeVersion` | `18.x` | Node.js версия для сборки |
| `routes[0]` | API proxy | Перенаправляет запросы на backend |
| `routes[1]` | SPA fallback | **КРИТИЧНО:** все маршруты → `/index.html` |

### ✅ Почему это работает:

1. **Build:** `npm run build` создает `dist/` папку с `index.html`
2. **SPA Routing:** Все маршруты перенаправляются на `index.html`
3. **React Router:** React Router ловит маршрут и показывает нужный компонент
4. **HTTPS:** Vercel автоматически предоставляет HTTPS с SSL сертификатом
5. **Camera API:** HTTPS ✓ → camera работает на мобильном

---

## React компонент

### CameraComponent.jsx - Полный пример с камерой

```jsx
/**
 * Advanced Camera Component for Cow Recognition
 * Supports mobile devices with proper error handling and HTTPS detection
 */

import React, { useRef, useState, useEffect } from 'react';

export default function CameraComponent() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  // State
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [cameraInfo, setCameraInfo] = useState(null);

  /**
   * STEP 1: Проверить поддержку камеры
   */
  useEffect(() => {
    const checkCameraSupport = () => {
      const supported = !!(
        navigator.mediaDevices &&
        navigator.mediaDevices.getUserMedia
      );

      const info = {
        supported,
        isHttps: window.location.protocol === 'https:',
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        browser: getBrowserInfo(),
        timestamp: new Date().toLocaleString('ru-RU')
      };

      setCameraInfo(info);
      console.log('[CameraComponent] Device Info:', info);

      if (!supported) {
        setError('❌ Ваше устройство не поддерживает доступ к камере');
      }

      if (!info.isHttps && window.location.hostname !== 'localhost') {
        setError(
          '⚠️ Требуется HTTPS для доступа к камере.\n' +
          'Используйте: https://yourdomain.com или localhost'
        );
      }
    };

    checkCameraSupport();
  }, []);

  /**
   * STEP 2: Определить браузер
   */
  const getBrowserInfo = () => {
    const ua = navigator.userAgent;
    if (ua.match(/edg/i)) return 'Edge';
    if (ua.match(/chrome|chromium|crios/i)) return 'Chrome';
    if (ua.match(/safari/i)) return 'Safari';
    if (ua.match(/opr\//i)) return 'Opera';
    if (ua.match(/firefox|fxios/i)) return 'Firefox';
    return 'Unknown';
  };

  /**
   * STEP 3: Открыть камеру
   */
  const openCamera = async () => {
    setIsLoading(true);
    setError(null);

    try {
      console.log('[CameraComponent] Requesting camera access...');

      // Запросить камеру с параметрами
      const constraints = {
        video: {
          facingMode: 'environment', // Задняя камера
          width: { ideal: 1280 },
          height: { ideal: 720 },
          aspectRatio: { ideal: 16 / 9 }
        },
        audio: false
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);

      if (!videoRef.current) {
        throw new Error('Video ref не найден');
      }

      // Подключить видеопоток
      videoRef.current.srcObject = stream;
      streamRef.current = stream;

      // iOS requires playsinline attribute
      if (videoRef.current.tagName === 'VIDEO') {
        videoRef.current.setAttribute('playsinline', 'true');
      }

      setIsCameraOpen(true);
      console.log('[CameraComponent] Camera opened successfully');
    } catch (err) {
      console.error('[CameraComponent] Camera error:', err);

      // Определить тип ошибки
      let errorMessage = 'Ошибка при открытии камеры: ';

      if (err.name === 'NotAllowedError') {
        errorMessage +=
          '🔒 Доступ к камере запрещен.\n' +
          'Разрешите доступ в настройках браузера.';
      } else if (err.name === 'NotFoundError') {
        errorMessage +=
          '📷 Камера не найдена на устройстве.';
      } else if (err.name === 'SecurityError') {
        errorMessage +=
          '🔐 Ошибка безопасности.\n' +
          'Требуется HTTPS для доступа к камере.';
      } else if (err.name === 'NotReadableError') {
        errorMessage +=
          '⚠️ Камера занята другим приложением.\n' +
          'Закройте другие приложения с камерой.';
      } else {
        errorMessage += err.message;
      }

      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * STEP 4: Закрыть камеру
   */
  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setIsCameraOpen(false);
    setCapturedImage(null);
    console.log('[CameraComponent] Camera closed');
  };

  /**
   * STEP 5: Снять фото
   */
  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) {
      setError('❌ Видео или canvas элемент не найдены');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    // Установить размеры canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Нарисовать кадр из видео на canvas
    ctx.drawImage(video, 0, 0);

    // Получить изображение в виде Data URL
    const imageDataUrl = canvas.toDataURL('image/jpeg', 0.95);
    setCapturedImage(imageDataUrl);

    console.log('[CameraComponent] Photo captured');

    // Закрыть камеру после снимка
    closeCamera();
  };

  /**
   * STEP 6: Отправить фото на сервер
   */
  const sendPhotoToServer = async () => {
    if (!capturedImage) {
      setError('❌ Нет захваченного фото');
      return;
    }

    setIsLoading(true);

    try {
      console.log('[CameraComponent] Sending photo to server...');

      // Конвертировать Data URL в Blob
      const response = await fetch(capturedImage);
      const blob = await response.blob();

      // Создать FormData
      const formData = new FormData();
      formData.append('file', blob, 'photo.jpg');

      // Отправить на сервер
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const uploadResponse = await fetch(`${apiUrl}/api/recognize`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      });

      if (!uploadResponse.ok) {
        throw new Error(`Server error: ${uploadResponse.status}`);
      }

      const result = await uploadResponse.json();
      console.log('[CameraComponent] Recognition result:', result);

      if (result.recognized) {
        alert(
          `✅ Корова распознана!\n` +
          `ID: ${result.cow_id}\n` +
          `Имя: ${result.cow_name}\n` +
          `Уверенность: ${(result.confidence * 100).toFixed(2)}%`
        );
      } else {
        alert('❌ Корова не распознана');
      }
    } catch (err) {
      console.error('[CameraComponent] Upload error:', err);
      setError(`❌ Ошибка при отправке: ${err.message}`);
    } finally {
      setIsLoading(false);
      setCapturedImage(null);
    }
  };

  /**
   * RENDER
   */
  return (
    <div className="w-full max-w-2xl mx-auto p-4 bg-white rounded-lg shadow">
      {/* Header */}
      <h1 className="text-3xl font-bold text-center mb-6">📷 Распознавание коров</h1>

      {/* Device Info (для отладки) */}
      {cameraInfo && (
        <div className="text-sm text-gray-600 mb-4 p-3 bg-gray-100 rounded">
          <p>🔹 Browser: {cameraInfo.browser}</p>
          <p>🔹 HTTPS: {cameraInfo.isHttps ? '✅ Да' : '❌ Нет'}</p>
          <p>🔹 Platform: {cameraInfo.platform}</p>
          <p>🔹 Supported: {cameraInfo.supported ? '✅ Да' : '❌ Нет'}</p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          <p className="font-bold">Ошибка:</p>
          <p className="whitespace-pre-line">{error}</p>
        </div>
      )}

      {/* Camera View или Captured Image */}
      <div className="mb-6 relative bg-black rounded-lg overflow-hidden aspect-video">
        {isCameraOpen ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
          />
        ) : capturedImage ? (
          <img
            src={capturedImage}
            alt="Captured"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-white">
            <p>📷 Нажми "Открыть камеру" для начала</p>
          </div>
        )}
      </div>

      {/* Hidden Canvas для захвата кадра */}
      <canvas
        ref={canvasRef}
        className="hidden"
      />

      {/* Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {!isCameraOpen && !capturedImage && (
          <button
            onClick={openCamera}
            disabled={isLoading || !cameraInfo?.supported}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
          >
            {isLoading ? '⏳ Загрузка...' : '📷 Открыть камеру'}
          </button>
        )}

        {isCameraOpen && (
          <>
            <button
              onClick={capturePhoto}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition"
            >
              ✅ Снять фото
            </button>
            <button
              onClick={closeCamera}
              className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-lg transition"
            >
              ❌ Закрыть
            </button>
          </>
        )}

        {capturedImage && (
          <>
            <button
              onClick={sendPhotoToServer}
              disabled={isLoading}
              className="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white font-bold rounded-lg transition"
            >
              {isLoading ? '⏳ Отправка...' : '🚀 Отправить'}
            </button>
            <button
              onClick={() => {
                setCapturedImage(null);
                openCamera();
              }}
              className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-lg transition"
            >
              🔄 Переснять
            </button>
          </>
        )}
      </div>
    </div>
  );
}
```

### Использование в App.jsx:

```jsx
import CameraComponent from './components/CameraComponent';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <CameraComponent />
    </div>
  );
}

export default App;
```

---

## Пошаговый деплой

### СПОСОБ 1: Деплой через Vercel CLI (Рекомендуется)

```bash
# 1. Перейти в папку frontend
cd C:\Users\user\Desktop\CowID\frontend

# 2. Установить Vercel CLI (если еще не установлен)
npm install -g vercel

# 3. Логин в Vercel (только первый раз)
vercel login

# Откроется браузер, авторизуйся с GitHub/GitLab/Email

# 4. Собрать Production build
npm run build

# Результат: создается папка "dist/" с готовым кодом

# 5. Развернуть на Vercel
vercel --prod

# Результат: https://cowid-frontend.vercel.app (или твое имя проекта)
```

### СПОСОБ 2: Деплой через GitHub (Автоматический)

```bash
# 1. Инициализировать git (если еще не сделал)
git init
git add .
git commit -m "Initial commit: CowID app"

# 2. Создать репо на GitHub
# https://github.com/new

# 3. Залить код на GitHub
git remote add origin https://github.com/твой-юзер/cowid-frontend.git
git branch -M main
git push -u origin main

# 4. На Vercel.com:
# - Нажать "New Project"
# - Выбрать репо "cowid-frontend"
# - Vercel автоматически обнаружит Vite
# - Нажать "Deploy"

# Результат: Автоматический деплой при каждом push в main
```

### СПОСОБ 3: Деплой через Vercel UI (Веб-интерфейс)

1. Перейти на [vercel.com](https://vercel.com)
2. Нажать "New Project"
3. Выбрать "Import Git Repository"
4. Выбрать твой GitHub репо
5. Vercel автоматически заполнит настройки:
   - Framework: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Нажать "Deploy"

---

## Мобильное тестирование

### Как открыть на телефоне

```
https://cowid-frontend.vercel.app
```

**✅ ВАЖНО:**
- Ссылка должна быть **HTTPS** (с замочком 🔒)
- **Не** `http://` - камера не будет работать!
- Vercel автоматически предоставляет HTTPS

### Шаги:

1. **На смартфоне:** Открыть браузер (Chrome, Safari, Firefox)

2. **Адресная строка:** Вставить ссылку
   ```
   https://cowid-frontend.vercel.app
   ```

3. **Разрешение:** Браузер спросит разрешение на камеру
   ```
   "CowID" хочет получить доступ к камере
   ```

4. **Нажать:** "Разрешить" / "Allow"

5. **Камера работает!** 📷
   - Видно видеопоток в реальном времени
   - Можно двигать телефон и видеть изменения
   - Нажать "Снять фото" → захватит кадр

---

## Troubleshooting

### ❌ "Камера не работает"

**Проверить:**

```
1. HTTPS? 
   ✓ https://cowid-frontend.vercel.app
   ✗ http://localhost:5173

2. Браузер разрешил доступ?
   iOS: Settings → Safari → Camera → ON
   Android: Settings → Apps → Chrome → Permissions → Camera

3. Камера не занята?
   Закрыть: WhatsApp, Telegram, Zoom, другие видео-приложения

4. Браузер поддерживает?
   ✓ Chrome (Android)
   ✓ Safari (iOS 12.2+)
   ✓ Firefox
   ✓ Edge
```

### ❌ "NotAllowedError"

```
Причина: Браузер запросил разрешение, но ты отказал

Решение:
- iOS: Settings → Safari → Camera → Allow для cowid-frontend.vercel.app
- Android: Settings → Apps → Chrome → Permissions → Camera → Allow
```

### ❌ "SecurityError / HTTPS required"

```
Причина: Камера требует HTTPS

Решение:
- Используй Vercel (автоматически HTTPS)
- Или localhost (работает без HTTPS только на desktop)
- Или ngrok для локального тестирования
```

### ❌ "Slow camera load"

```
Причина: Плохой интернет или тяжелый браузер

Решение:
- Подключиться к быстрому Wi-Fi
- Закрыть другие вкладки
- Перезагрузить браузер (F5)
- Очистить кэш браузера
```

---

## 📊 Финальный Чеклист

### Перед Деплоем

- [ ] `npm run build` успешно (создана папка `dist/`)
- [ ] `vercel login` успешно (авторизирован в Vercel)
- [ ] `vercel.json` существует и корректен
- [ ] `.gitignore` исключает `dist/` и `.vercel/`

### Во время Деплоя

- [ ] `vercel --prod` без ошибок
- [ ] Vercel показывает URL: `https://cowid-xxx.vercel.app`
- [ ] Деплой завершен (зеленая галочка)

### После Деплоя (Desktop)

- [ ] Ссылка открывается в браузере
- [ ] Видна главная страница приложения
- [ ] Кнопка "Открыть камеру" видна
- [ ] Консоль (F12) не показывает ошибок

### На Мобильном Устройстве

- [ ] Открыл HTTPS ссылку (не HTTP)
- [ ] Браузер спросил разрешение на камеру
- [ ] Дал разрешение → видно видеопоток
- [ ] Нажал "Снять фото" → фото захвачено
- [ ] Нажал "Отправить" → система распознала корову

### Если Все ✅

```
🎉 УСПЕШНО!

Frontend развернут на Vercel ✅
Камера работает на мобильном ✅
Приложение готово к использованию ✅
```

---

**Версия:** 1.0.0  
**Дата:** 2026-02-04  
**Поддерживаемые браузеры:** Chrome, Safari, Firefox, Edge  
**Минимальная iOS:** 12.2  
**Минимальная Android:** 5.0

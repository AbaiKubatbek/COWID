/**
 * Advanced Camera Component for Cow Recognition
 * 
 * Полнофункциональный компонент для захвата фото с камеры мобильного устройства
 * с полной поддержкой ошибок, отладки и мобильных браузеров
 * 
 * Использование:
 * import CameraComponent from './components/CameraComponent';
 * 
 * export default function App() {
 *   return <CameraComponent />;
 * }
 * 
 * Требования:
 * - Vite + React 18+
 * - Tailwind CSS (для стилей, опционально)
 * - HTTPS (для камеры на мобильном)
 */

import React, { useRef, useState, useEffect } from 'react';

export default function CameraComponent() {
  // ============ REFS ============
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);

  // ============ STATE ============
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [cameraInfo, setCameraInfo] = useState(null);
  const [recognitionResult, setRecognitionResult] = useState(null);

  // ============ LIFECYCLE ============
  useEffect(() => {
    checkCameraSupport();
    return () => {
      // Cleanup: закрыть камеру при размонтировании компонента
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  // ============ FUNCTIONS ============

  /**
   * Проверить поддержку камеры на устройстве
   */
  const checkCameraSupport = () => {
    const supported = !!(
      navigator.mediaDevices &&
      navigator.mediaDevices.getUserMedia
    );

    const isHttps = window.location.protocol === 'https:';
    const userAgent = navigator.userAgent;
    
    const info = {
      supported,
      isHttps,
      userAgent,
      platform: navigator.platform,
      browser: getBrowserInfo(),
      isIOS: /iPad|iPhone|iPod/.test(userAgent),
      isAndroid: /Android/.test(userAgent),
      timestamp: new Date().toLocaleString('ru-RU')
    };

    setCameraInfo(info);
    console.log('[CameraComponent] Device Info:', info);

    if (!supported) {
      setError('❌ Ваше устройство не поддерживает доступ к камере');
    }

    if (!isHttps && window.location.hostname !== 'localhost') {
      setError(
        '⚠️ HTTPS требуется для доступа к камере.\n' +
        `Вы используете: ${window.location.protocol}\n` +
        'Используйте: https://yourdomain.com или localhost'
      );
    }
  };

  /**
   * Определить браузер пользователя
   */
  const getBrowserInfo = () => {
    const ua = navigator.userAgent;
    if (ua.match(/edg/i)) return 'Microsoft Edge';
    if (ua.match(/chrome|chromium|crios/i)) return 'Google Chrome';
    if (ua.match(/safari/i)) return 'Apple Safari';
    if (ua.match(/opr\//i)) return 'Opera';
    if (ua.match(/firefox|fxios/i)) return 'Mozilla Firefox';
    return 'Unknown Browser';
  };

  /**
   * Открыть камеру
   */
  const openCamera = async () => {
    setIsLoading(true);
    setError(null);
    setRecognitionResult(null);

    try {
      console.log('[CameraComponent] Requesting camera access...');

      // Параметры для получения видеопотока
      const constraints = {
        video: {
          facingMode: 'environment', // Задняя камера
          width: { ideal: 1280 },
          height: { ideal: 720 },
          aspectRatio: { ideal: 16 / 9 }
        },
        audio: false
      };

      // Запросить камеру
      const stream = await navigator.mediaDevices.getUserMedia(constraints);

      if (!videoRef.current) {
        throw new Error('Video element reference not found');
      }

      // Подключить видеопоток к <video> элементу
      videoRef.current.srcObject = stream;
      streamRef.current = stream;

      // iOS требует playsinline для работы видео в fullscreen mode
      if (videoRef.current.tagName === 'VIDEO') {
        videoRef.current.setAttribute('playsinline', 'true');
        videoRef.current.setAttribute('autoplay', 'true');
        videoRef.current.setAttribute('muted', 'true');
      }

      setIsCameraOpen(true);
      console.log('[CameraComponent] ✅ Camera opened successfully');
    } catch (err) {
      console.error('[CameraComponent] Camera error:', err);
      handleCameraError(err);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Обработать ошибки камеры
   */
  const handleCameraError = (err) => {
    let errorMessage = '❌ Ошибка при открытии камеры:\n\n';

    switch (err.name) {
      case 'NotAllowedError':
        errorMessage +=
          '🔒 Доступ к камере запрещен браузером.\n\n' +
          'Решение:\n' +
          '• iOS: Settings → Safari → Camera → Allow\n' +
          '• Android: Settings → Apps → Chrome → Permissions → Camera\n' +
          '• Перезагрузи браузер и попробуй еще раз';
        break;

      case 'NotFoundError':
        errorMessage +=
          '📷 Камера не найдена на устройстве.\n\n' +
          'Проверь:\n' +
          '• Есть ли физическая камера\n' +
          '• Не сломана ли камера\n' +
          '• Работает ли в других приложениях';
        break;

      case 'SecurityError':
        errorMessage +=
          '🔐 Ошибка безопасности.\n\n' +
          'Требуется HTTPS для доступа к камере.\n' +
          `Ты используешь: ${window.location.protocol}\n\n` +
          'Используй:\n' +
          '• https://yourdomain.com (production)\n' +
          '• https://localhost (с самоподписанным сертификатом)\n' +
          '• Vercel (автоматически HTTPS)';
        break;

      case 'NotReadableError':
        errorMessage +=
          '⚠️ Камера занята другим приложением.\n\n' +
          'Закрой:\n' +
          '• WhatsApp, Telegram, Zoom\n' +
          '• Другие видео-приложения\n' +
          '• Другие вкладки браузера с камерой';
        break;

      case 'OverconstrainedError':
        errorMessage +=
          '📐 Устройство не поддерживает запрошенные параметры.\n' +
          'Пробую с базовыми параметрами...';
        // Retry with basic constraints
        retryWithBasicConstraints();
        return;

      default:
        errorMessage += err.message || 'Unknown error';
    }

    setError(errorMessage);
  };

  /**
   * Повторить с базовыми параметрами (для совместимости)
   */
  const retryWithBasicConstraints = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
        videoRef.current.setAttribute('playsinline', 'true');
        setIsCameraOpen(true);
        setError(null);
      }
    } catch (err) {
      handleCameraError(err);
    }
  };

  /**
   * Закрыть камеру
   */
  const closeCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
        console.log('[CameraComponent] Track stopped:', track.kind);
      });
      streamRef.current = null;
    }
    setIsCameraOpen(false);
    console.log('[CameraComponent] Camera closed');
  };

  /**
   * Снять фото с видеопотока
   */
  const capturePhoto = () => {
    if (!videoRef.current) {
      setError('❌ Видео элемент не найден');
      return;
    }

    if (!canvasRef.current) {
      setError('❌ Canvas элемент не найден');
      return;
    }

    try {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      if (!ctx) {
        throw new Error('Cannot get 2D context');
      }

      // Установить размеры canvas = размеры видео
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      console.log(
        `[CameraComponent] Capturing ${canvas.width}x${canvas.height}`
      );

      // Нарисовать текущий кадр видео на canvas
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Получить изображение в виде Data URL (JPEG)
      const imageDataUrl = canvas.toDataURL('image/jpeg', 0.95);
      setCapturedImage(imageDataUrl);

      console.log('[CameraComponent] ✅ Photo captured');

      // Закрыть камеру после захвата
      closeCamera();
    } catch (err) {
      console.error('[CameraComponent] Capture error:', err);
      setError(`❌ Ошибка при захвате фото: ${err.message}`);
    }
  };

  /**
   * Отправить фото на сервер для распознавания
   */
  const sendPhotoToServer = async () => {
    if (!capturedImage) {
      setError('❌ Нет захваченного фото');
      return;
    }

    setIsLoading(true);
    setError(null);
    setRecognitionResult(null);

    try {
      console.log('[CameraComponent] Sending photo to server...');

      // Конвертировать Data URL в Blob
      const response = await fetch(capturedImage);
      const blob = await response.blob();

      // Создать FormData
      const formData = new FormData();
      formData.append('file', blob, 'photo.jpg');

      // Получить URL API
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      console.log('[CameraComponent] API URL:', apiUrl);

      // Отправить POST запрос
      const uploadResponse = await fetch(`${apiUrl}/api/recognize`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json'
          // 'Content-Type': 'multipart/form-data' - браузер установит автоматически
        }
      });

      if (!uploadResponse.ok) {
        throw new Error(`Server error: ${uploadResponse.status}`);
      }

      const result = await uploadResponse.json();
      console.log('[CameraComponent] ✅ Recognition result:', result);

      setRecognitionResult(result);

      // Показать результат пользователю
      if (result.recognized) {
        // eslint-disable-next-line no-undef
        alert(
          `✅ Корова распознана!\n\n` +
          `ID: ${result.cow_id}\n` +
          `Имя: ${result.cow_name}\n` +
          `Уверенность: ${(result.confidence * 100).toFixed(2)}%`
        );
      } else {
        // eslint-disable-next-line no-undef
        alert('❌ Корова не распознана. Попробуй еще раз.');
      }
    } catch (err) {
      console.error('[CameraComponent] Upload error:', err);
      setError(`❌ Ошибка при отправке: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Переснять фото (открыть камеру заново)
   */
  const retakePhoto = () => {
    setCapturedImage(null);
    setRecognitionResult(null);
    openCamera();
  };

  /**
   * RENDER
   */
  return (
    <div className="w-full max-w-4xl mx-auto p-4">
      {/* ============ HEADER ============ */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          📷 Распознавание коров
        </h1>
        <p className="text-gray-600">
          Снимай фото коровы через камеру — система распознает ее мгновенно
        </p>
      </div>

      {/* ============ DEVICE INFO (для отладки) ============ */}
      {cameraInfo && (
        <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg text-sm">
          <p className="font-bold text-blue-900 mb-2">ℹ️ Информация об устройстве:</p>
          <div className="grid grid-cols-2 gap-2 text-blue-800">
            <p>🔹 Browser: {cameraInfo.browser}</p>
            <p>🔹 HTTPS: {cameraInfo.isHttps ? '✅ Да' : '❌ Нет'}</p>
            <p>🔹 Platform: {cameraInfo.platform}</p>
            <p>🔹 iOS: {cameraInfo.isIOS ? '✅ Да' : '❌ Нет'}</p>
            <p>🔹 Android: {cameraInfo.isAndroid ? '✅ Да' : '❌ Нет'}</p>
            <p>🔹 Поддержка: {cameraInfo.supported ? '✅ Да' : '❌ Нет'}</p>
          </div>
        </div>
      )}

      {/* ============ ERROR MESSAGE ============ */}
      {error && (
        <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
          <p className="font-bold mb-2">⚠️ Ошибка:</p>
          <p className="whitespace-pre-line text-sm">{error}</p>
        </div>
      )}

      {/* ============ RECOGNITION RESULT ============ */}
      {recognitionResult && (
        <div className={`mb-6 p-4 rounded-lg border-2 ${
          recognitionResult.recognized
            ? 'bg-green-100 border-green-400 text-green-700'
            : 'bg-yellow-100 border-yellow-400 text-yellow-700'
        }`}>
          <p className="font-bold mb-2">
            {recognitionResult.recognized ? '✅ Результат распознавания' : '⚠️ Результат'}
          </p>
          {recognitionResult.recognized ? (
            <div className="text-sm">
              <p>🐄 Имя: {recognitionResult.cow_name}</p>
              <p>🆔 ID: {recognitionResult.cow_id}</p>
              <p>📊 Уверенность: {(recognitionResult.confidence * 100).toFixed(2)}%</p>
            </div>
          ) : (
            <p className="text-sm">Корова не распознана. Попробуй еще раз.</p>
          )}
        </div>
      )}

      {/* ============ VIDEO/IMAGE VIEW ============ */}
      <div className="mb-6 relative bg-black rounded-lg overflow-hidden aspect-video shadow-lg">
        {isCameraOpen ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className="w-full h-full object-cover"
            onLoadedMetadata={() => console.log('[CameraComponent] Video loaded')}
            onError={(e) => console.error('[CameraComponent] Video error:', e)}
          />
        ) : capturedImage ? (
          <img
            src={capturedImage}
            alt="Captured cow"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex flex-col items-center justify-center text-white">
            <p className="text-2xl mb-2">📷</p>
            <p>Нажми "Открыть камеру" для начала</p>
          </div>
        )}
      </div>

      {/* ============ HIDDEN CANVAS ============ */}
      <canvas ref={canvasRef} className="hidden" />

      {/* ============ BUTTONS ============ */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Camera closed - show open button */}
        {!isCameraOpen && !capturedImage && (
          <button
            onClick={openCamera}
            disabled={isLoading || !cameraInfo?.supported}
            className={`px-6 py-3 rounded-lg font-bold text-white transition ${
              isLoading || !cameraInfo?.supported
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
            }`}
          >
            {isLoading ? '⏳ Загрузка...' : '📷 Открыть камеру'}
          </button>
        )}

        {/* Camera open - show capture and close buttons */}
        {isCameraOpen && (
          <>
            <button
              onClick={capturePhoto}
              className="px-6 py-3 rounded-lg font-bold text-white bg-green-600 hover:bg-green-700 active:scale-95 transition"
            >
              ✅ Снять фото
            </button>
            <button
              onClick={closeCamera}
              className="px-6 py-3 rounded-lg font-bold text-white bg-red-600 hover:bg-red-700 active:scale-95 transition"
            >
              ❌ Закрыть
            </button>
          </>
        )}

        {/* Photo captured - show send and retake buttons */}
        {capturedImage && (
          <>
            <button
              onClick={sendPhotoToServer}
              disabled={isLoading}
              className={`px-6 py-3 rounded-lg font-bold text-white transition ${
                isLoading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-purple-600 hover:bg-purple-700 active:scale-95'
              }`}
            >
              {isLoading ? '⏳ Отправка...' : '🚀 Отправить'}
            </button>
            <button
              onClick={retakePhoto}
              className="px-6 py-3 rounded-lg font-bold text-white bg-blue-600 hover:bg-blue-700 active:scale-95 transition"
            >
              🔄 Переснять
            </button>
          </>
        )}
      </div>

      {/* ============ FOOTER ============ */}
      <div className="mt-8 p-4 bg-gray-100 rounded-lg text-center text-sm text-gray-600">
        <p>
          💡 Совет: Для лучшего распознавания снимай морду коровы четко
          при хорошем освещении с расстояния 1-3 метра
        </p>
      </div>
    </div>
  );
}

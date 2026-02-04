/**
 * Camera utilities for capturing photos from device camera
 * 
 * ТРЕБОВАНИЯ ДЛЯ РАБОТЫ:
 * 1. ✓ HTTPS (медиа API требует безопасности)
 * 2. ✓ Разрешение от юзера (браузер спросит)
 * 3. ✓ Поддержка getUserMedia (Chrome, Safari, Firefox)
 */

/**
 * Opens camera and captures a photo
 * @returns {Promise<Blob>} Image blob or null if cancelled
 */
export const capturePhotoFromCamera = async () => {
  try {
    // Проверяем поддержку
    if (!isCameraSupported()) {
      throw new Error('Ваш браузер не поддерживает доступ к камере');
    }

    // Запрашиваем доступ к камере
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: 'environment',  // Задняя камера на мобильных
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false  // Микрофон не нужен
    });

    return new Promise((resolve, reject) => {
      // Создаем video element
      const video = document.createElement('video');
      video.srcObject = stream;
      video.setAttribute('playsinline', 'true');  // iOS требует
      video.play();

      // Ждем когда видео будет готово
      video.onloadedmetadata = () => {
        // Создаем canvas
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Рисуем кадр видео на canvas
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);

        // Останавливаем поток камеры
        stream.getTracks().forEach(track => track.stop());

        // Конвертируем canvas в Blob
        canvas.toBlob(
          blob => {
            if (blob) {
              console.log('✅ Фото захвачено:', blob.size, 'bytes');
              resolve(blob);
            } else {
              reject(new Error('Не удалось захватить фото'));
            }
          },
          'image/jpeg',
          0.95  // Качество 95%
        );
      };

      video.onerror = (error) => {
        stream.getTracks().forEach(track => track.stop());
        reject(new Error(`Ошибка видео: ${error.message}`));
      };

      // Timeout если видео не загружается
      setTimeout(() => {
        if (!video.srcObject) return;
        stream.getTracks().forEach(track => track.stop());
        reject(new Error('Timeout при загрузке видео'));
      }, 10000);
    });
  } catch (error) {
    // Определяем причину ошибки
    let userMessage = '';

    if (error.name === 'NotAllowedError') {
      userMessage = '❌ Вы запретили доступ к камере. Разрешите в настройках браузера.';
    } else if (error.name === 'NotFoundError') {
      userMessage = '❌ Камера не найдена на устройстве';
    } else if (error.name === 'NotReadableError') {
      userMessage = '❌ Камера занята другим приложением';
    } else if (error.name === 'SecurityError' || error.message?.includes('https')) {
      userMessage = '❌ Требуется HTTPS для доступа к камере (вы на http://)';
    } else {
      userMessage = `❌ Ошибка камеры: ${error.message}`;
    }

    console.error('Camera error:', error);
    throw new Error(userMessage);
  }
};

/**
 * Проверяет поддержку камеры браузером
 * @returns {boolean}
 */
export const isCameraSupported = () => {
  return !!(
    navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia
  );
};

/**
 * Конвертирует Blob в File объект
 * @param {Blob} blob
 * @param {string} fileName
 * @returns {File}
 */
export const blobToFile = (blob, fileName = 'photo.jpg') => {
  return new File([blob], fileName, { type: 'image/jpeg' });
};

/**
 * Получает информацию о устройстве и браузере
 * @returns {Object} информация о поддержке
 */
export const getCameraInfo = () => {
  return {
    isHttps: window.location.protocol === 'https:',
    isCameraSupported: isCameraSupported(),
    userAgent: navigator.userAgent,
    isIOS: /iPad|iPhone|iPod/.test(navigator.userAgent),
    isAndroid: /Android/.test(navigator.userAgent),
    browser: getBrowserName()
  };
};

/**
 * Определяет название браузера
 * @returns {string}
 */
function getBrowserName() {
  const ua = navigator.userAgent;
  
  if (ua.includes('Chrome')) return 'Chrome';
  if (ua.includes('Safari')) return 'Safari';
  if (ua.includes('Firefox')) return 'Firefox';
  if (ua.includes('Edge')) return 'Edge';
  return 'Unknown';
}

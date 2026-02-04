/**
 * Camera Modal Component for capturing photos
 */

import React, { useRef, useState } from 'react';
import { capturePhotoFromCamera, isCameraSupported, blobToFile } from '../utils/cameraUtils';

export default function CameraModal({ isOpen, onClose, onCapture }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);

  const startCamera = async () => {
    if (!isCameraSupported()) {
      setError('Ваше устройство не поддерживает доступ к камере');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        streamRef.current = stream;
      }
    } catch (err) {
      setError(`Ошибка доступа к камере: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL('image/jpeg', 0.95);
    setCapturedImage(imageData);
  };

  const confirmCapture = () => {
    if (!canvasRef.current) return;

    canvasRef.current.toBlob(
      blob => {
        if (blob) {
          const file = blobToFile(blob);
          onCapture(file);
          handleClose();
        }
      },
      'image/jpeg',
      0.95
    );
  };

  const handleClose = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setCapturedImage(null);
    setError(null);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-md w-full">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-4">📷 Снимок с камеры</h2>

          {error && (
            <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 mb-4">
              {error}
            </div>
          )}

          {!capturedImage ? (
            <>
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full bg-black rounded-lg mb-4"
                onLoadedMetadata={startCamera}
              />

              <canvas ref={canvasRef} className="hidden" />

              <button
                onClick={capturePhoto}
                disabled={isLoading || !streamRef.current}
                className="w-full bg-green-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {isLoading ? '⏳ Загрузка...' : '📷 Сделать фото'}
              </button>
            </>
          ) : (
            <>
              <img
                src={capturedImage}
                alt="Captured"
                className="w-full rounded-lg mb-4"
              />

              <div className="flex gap-2">
                <button
                  onClick={() => setCapturedImage(null)}
                  className="flex-1 bg-gray-400 text-white py-2 px-4 rounded-lg font-semibold hover:bg-gray-500 transition"
                >
                  🔄 Пересснять
                </button>
                <button
                  onClick={confirmCapture}
                  className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-700 transition"
                >
                  ✓ Использовать
                </button>
              </div>
            </>
          )}

          <button
            onClick={handleClose}
            className="w-full mt-3 bg-gray-300 text-gray-700 py-2 px-4 rounded-lg font-semibold hover:bg-gray-400 transition"
          >
            ✕ Закрыть
          </button>
        </div>
      </div>
    </div>
  );
}

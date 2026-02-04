/**
 * Компонент для загрузки изображения и распознавания коров
 */

import React, { useState, useRef } from 'react';
import { recognizeFromImage } from '../services/api';
import { useRecognitionStore } from '../store/store';
import MedicalCard from './MedicalCard';
import CameraModal from './CameraModal';

export default function RecognitionForm() {
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  
  const { recognitionResult, setRecognitionResult, setRecognitionError } = useRecognitionStore();

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    setSelectedFile(file);
    
    // Создаём preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
    };
    reader.readAsDataURL(file);
  };

  const handleCameraCapture = (file) => {
    processFile(file);
  };

  const handleRecognize = async () => {
    if (!selectedFile) {
      setRecognitionError('Пожалуйста выберите изображение');
      return;
    }

    setIsLoading(true);
    setRecognitionError(null);

    try {
      const result = await recognizeFromImage(selectedFile);
      setRecognitionResult(result);
    } catch (error) {
      setRecognitionError(error.response?.data?.detail || 'Ошибка при распознавании');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8 text-white">
        🐄 Распознавание коров
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Загрузка изображения */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-semibold mb-4">Загрузить фото</h2>
          
          {/* Preview */}
          {preview ? (
            <div className="mb-4">
              <img 
                src={preview} 
                alt="Preview" 
                className="w-full h-64 object-cover rounded-lg"
              />
            </div>
          ) : (
            <div 
              className="w-full h-64 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center mb-4 cursor-pointer hover:border-green-500 transition"
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="text-center">
                <p className="text-gray-500 text-lg">📸 Нажмите для загрузки</p>
                <p className="text-gray-400 text-sm">или перетащите файл</p>
              </div>
            </div>
          )}

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
          />

          <div className="space-y-2 mb-4">
            <button
              onClick={() => fileInputRef.current?.click()}
              className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition font-medium"
            >
              📁 Выбрать файл
            </button>

            <button
              onClick={() => setIsCameraOpen(true)}
              className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition font-medium"
            >
              📷 Открыть камеру
            </button>
          </div>

          {selectedFile && (
            <p className="text-sm text-gray-600 mb-4">
              Выбрано: {selectedFile.name}
            </p>
          )}

          <button
            onClick={handleRecognize}
            disabled={!selectedFile || isLoading}
            className="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-semibold hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
          >
            {isLoading ? '⏳ Распознавание...' : '🔍 Распознать'}
          </button>
        </div>

        {/* Результат */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          {recognitionResult ? (
            <>
              {recognitionResult.success ? (
                <div className="bg-green-50 border-l-4 border-green-500 p-4 mb-4">
                  <p className="text-green-700 font-semibold">
                    ✅ {recognitionResult.message}
                  </p>
                  <p className="text-green-600 mt-2">
                    Уверенность: {(recognitionResult.confidence * 100).toFixed(1)}%
                  </p>
                </div>
              ) : (
                <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 mb-4">
                  <p className="text-yellow-700 font-semibold">
                    ⚠️ {recognitionResult.message}
                  </p>
                </div>
              )}

              {recognitionResult.cow && (
                <MedicalCard cow={recognitionResult.cow} />
              )}
            </>
          ) : (
            <div className="text-center text-gray-500">
              <p className="text-lg">👀 Результаты появятся здесь</p>
            </div>
          )}
        </div>
      </div>

      {/* Camera Modal */}
      <CameraModal 
        isOpen={isCameraOpen}
        onClose={() => setIsCameraOpen(false)}
        onCapture={handleCameraCapture}
      />
    </div>
  );
}

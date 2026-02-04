/**
 * Главный компонент приложения
 */

import React, { useState } from 'react';
import { useUIStore } from './store/store';
import AdminPanel from './components/AdminPanel';
import RecognitionForm from './components/RecognitionForm';

function App() {
  const { currentPage, setCurrentPage } = useUIStore();

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#0B3D2E' }}>
      {/* Navigation */}
      <nav className="bg-gradient-to-r from-green-700 to-green-900 text-white shadow-lg">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🐄</span>
            <h1 className="text-2xl font-bold">CowID</h1>
          </div>
          
          <div className="flex gap-4">
            <button
              onClick={() => setCurrentPage('recognition')}
              className={`px-4 py-2 rounded transition ${
                currentPage === 'recognition'
                  ? 'bg-white text-green-700 font-semibold'
                  : 'hover:bg-green-800'
              }`}
            >
              🔍 Распознавание
            </button>
            <button
              onClick={() => setCurrentPage('admin')}
              className={`px-4 py-2 rounded transition ${
                currentPage === 'admin'
                  ? 'bg-white text-green-700 font-semibold'
                  : 'hover:bg-green-800'
              }`}
            >
              ⚙️ Admin
            </button>
            <button
              onClick={() => setCurrentPage('home')}
              className={`px-4 py-2 rounded transition ${
                currentPage === 'home'
                  ? 'bg-white text-green-700 font-semibold'
                  : 'hover:bg-green-800'
              }`}
            >
              🏠 Главная
            </button>
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="py-8">
        {currentPage === 'home' && (
          <div className="max-w-4xl mx-auto text-center px-4">
            <h1 className="text-5xl font-bold text-white mb-6">
              🐄 Добро пожаловать в CowID
            </h1>
            <p className="text-xl text-white mb-8">
              Система интеллектуального распознавания лиц коров
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
              <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
                <p className="text-4xl mb-3">🔍</p>
                <h3 className="text-xl font-bold mb-2">Распознавание</h3>
                <p className="text-gray-600">
                  Загружайте фото морды коровы и получайте её информацию
                </p>
              </div>
              
              <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
                <p className="text-4xl mb-3">📷</p>
                <h3 className="text-xl font-bold mb-2">Камера</h3>
                <p className="text-gray-600">
                  Используйте камеру вашего устройства для мгновенного распознавания
                </p>
              </div>
              
              <div className="bg-white p-8 rounded-lg shadow-lg hover:shadow-xl transition">
                <p className="text-4xl mb-3">📋</p>
                <h3 className="text-xl font-bold mb-2">Медкарты</h3>
                <p className="text-gray-600">
                  Полная медицинская информация о каждой корове
                </p>
              </div>
            </div>

            <div className="mt-12 space-y-4">
              <button
                onClick={() => setCurrentPage('recognition')}
                className="bg-green-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-green-700 transition"
              >
                🔍 Начать распознавание
              </button>
              
              <button
                onClick={() => setCurrentPage('admin')}
                className="bg-green-500 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-green-600 transition ml-4"
              >
                ⚙️ Перейти в Admin
              </button>
            </div>
          </div>
        )}

        {currentPage === 'recognition' && <RecognitionForm />}

        {currentPage === 'admin' && <AdminPanel />}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white text-center py-6 mt-12">
        <p>CowID v1.0 - Система распознавания лиц коров на основе ИИ</p>
        <p className="text-gray-400 text-sm mt-2">
          Использует YOLOv8, ResNet50, PyTorch и FastAPI
        </p>
      </footer>
    </div>
  );
}

export default App;

/**
 * Admin панель для управления коовами (CRUD операции)
 */

import React, { useState, useEffect } from 'react';
import { getCows, createCow, updateCow, deleteCow, addMedicalRecord } from '../services/api';
import { useCowStore } from '../store/store';
import MedicalCard from './MedicalCard';
import CameraModal from './CameraModal';

export default function AdminPanel() {
  const { cows, setCows, currentCow, setCurrentCow } = useCowStore();
  const [isLoading, setIsLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [showMedicalForm, setShowMedicalForm] = useState(false);
  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [error, setError] = useState(null);
  
  // Форма для создания/редактирования коровы
  const [formData, setFormData] = useState({
    name: '',
    breed: '',
    age: '',
    weight: '',
    insemination_status: false,
    insemination_date: ''
  });
  const [photoFile, setPhotoFile] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);

  // Форма для медицинской записи
  const [medicalData, setMedicalData] = useState({
    record_type: 'vaccine',
    title: '',
    description: '',
    record_date: new Date().toISOString().split('T')[0]
  });

  // Загружаем коов при монтировании компонента
  useEffect(() => {
    loadCows();
  }, []);

  const loadCows = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getCows();
      setCows(data);
    } catch (err) {
      setError('Ошибка при загрузке коов');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleMedicalChange = (e) => {
    const { name, value } = e.target;
    setMedicalData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePhotoSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPhotoFile(file);
      const reader = new FileReader();
      reader.onload = (event) => {
        setPhotoPreview(event.target.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCameraCapture = (file) => {
    setPhotoFile(file);
    const reader = new FileReader();
    reader.onload = (event) => {
      setPhotoPreview(event.target.result);
    };
    reader.readAsArrayBuffer(file);
  };

  const handleAddCow = async () => {
    if (!formData.name || !formData.breed || !formData.age) {
      setError('Заполните все обязательные поля');
      return;
    }

    setIsLoading(true);
    try {
      const newCow = await createCow(formData, photoFile);
      setCows([...cows, newCow]);
      setFormData({ name: '', breed: '', age: '', weight: '' });
      setPhotoFile(null);
      setPhotoPreview(null);
      setShowForm(false);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при создании коовы');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpdateCow = async () => {
    if (!currentCow) return;

    setIsLoading(true);
    try {
      const updatedCow = await updateCow(currentCow.id, formData);
      setCows(cows.map(c => c.id === currentCow.id ? updatedCow : c));
      setCurrentCow(updatedCow);
      setShowForm(false);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при обновлении коовы');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteCow = async (cowId) => {
    if (!window.confirm('Вы уверены? Это действие нельзя отменить.')) return;

    setIsLoading(true);
    try {
      await deleteCow(cowId);
      setCows(cows.filter(c => c.id !== cowId));
      if (currentCow?.id === cowId) setCurrentCow(null);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при удалении коовы');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddMedicalRecord = async () => {
    if (!currentCow || !medicalData.title) {
      setError('Заполните все поля медицинской записи');
      return;
    }

    setIsLoading(true);
    try {
      const record = await addMedicalRecord(currentCow.id, {
        ...medicalData,
        record_date: new Date(medicalData.record_date).toISOString()
      });
      
      const updatedCow = {
        ...currentCow,
        medical_records: [...(currentCow.medical_records || []), record]
      };
      setCurrentCow(updatedCow);
      setCows(cows.map(c => c.id === currentCow.id ? updatedCow : c));
      
      setMedicalData({
        record_type: 'vaccine',
        title: '',
        description: '',
        record_date: new Date().toISOString().split('T')[0]
      });
      setShowMedicalForm(false);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Ошибка при добавлении медицинской записи');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSelectCow = (cow) => {
    setCurrentCow(cow);
    setFormData({
      name: cow.name,
      breed: cow.breed,
      age: cow.age.toString(),
      weight: cow.weight?.toString() || '',
      insemination_status: cow.insemination_status || false,
      insemination_date: cow.insemination_date ? cow.insemination_date.split('T')[0] : ''
    });
    setShowForm(false);
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h1 className="text-4xl font-bold mb-8 text-white">
        🐄 Admin панель - Управление коровами
      </h1>

      {error && (
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Список коров */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">Коровы ({cows.length})</h2>
              <button
                onClick={() => {
                  setShowForm(true);
                  setCurrentCow(null);
                  setFormData({ name: '', breed: '', age: '', weight: '', insemination_status: false, insemination_date: '' });
                  setPhotoFile(null);
                  setPhotoPreview(null);
                }}
                className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 transition text-sm font-medium"
              >
                + Добавить
              </button>
            </div>

            {isLoading && cows.length === 0 ? (
              <p className="text-gray-500 text-center py-4">Загрузка...</p>
            ) : (
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {cows.map(cow => (
                  <div
                    key={cow.id}
                    onClick={() => handleSelectCow(cow)}
                    className={`p-3 border rounded-lg cursor-pointer transition ${
                      currentCow?.id === cow.id
                        ? 'bg-green-50 border-green-500'
                        : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <p className="font-semibold">{cow.name}</p>
                    <p className="text-sm text-gray-600">
                      {cow.breed} • {cow.age}л
                    </p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Детали и форма */}
        <div className="lg:col-span-2">
          {currentCow && !showForm && !showMedicalForm ? (
            <div className="space-y-6">
              <MedicalCard cow={currentCow} />
              
              <div className="flex flex-col sm:flex-row gap-2">
                <button
                  onClick={() => setShowForm(true)}
                  className="flex-1 bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition font-medium"
                >
                  ✏️ Редактировать
                </button>
                <button
                  onClick={() => {
                    setShowMedicalForm(true);
                  }}
                  className="flex-1 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 transition font-medium"
                >
                  ➕ Медзапись
                </button>
                <button
                  onClick={() => handleDeleteCow(currentCow.id)}
                  className="flex-1 bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition font-medium"
                >
                  🗑️ Удалить
                </button>
              </div>
            </div>
          ) : showForm ? (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">
                {currentCow ? 'Редактировать корову' : 'Добавить новую корову'}
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Имя *</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleFormChange}
                    className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-200"
                    placeholder="Например: Bessie"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Порода *</label>
                  <input
                    type="text"
                    name="breed"
                    value={formData.breed}
                    onChange={handleFormChange}
                    className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-200"
                    placeholder="Например: Holstein"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold mb-2">Возраст (годы) *</label>
                    <input
                      type="number"
                      name="age"
                      value={formData.age}
                      onChange={handleFormChange}
                      className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-200"
                      placeholder="5"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-semibold mb-2">Вес (кг)</label>
                    <input
                      type="number"
                      name="weight"
                      value={formData.weight}
                      onChange={handleFormChange}
                      className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-200"
                      placeholder="600"
                    />
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h3 className="text-lg font-semibold mb-4 flex items-center">
                    <span className="mr-2">🔬</span>
                    Осеменение
                  </h3>
                  
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-semibold mb-2">Статус</label>
                      <select
                        name="insemination_status"
                        value={formData.insemination_status ? 'true' : 'false'}
                        onChange={(e) => handleFormChange({
                          target: {
                            name: 'insemination_status',
                            value: e.target.value === 'true'
                          }
                        })}
                        className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500"
                      >
                        <option value="false">✗ Нет</option>
                        <option value="true">✓ Да</option>
                      </select>
                    </div>

                    {formData.insemination_status && (
                      <div>
                        <label className="block text-sm font-semibold mb-2">Дата осеменения</label>
                        <input
                          type="date"
                          name="insemination_date"
                          value={formData.insemination_date}
                          onChange={handleFormChange}
                          className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500"
                        />
                      </div>
                    )}
                  </div>
                </div>

                {!currentCow && (
                  <div>
                    <label className="block text-sm font-semibold mb-3">Фото морды коровы</label>
                    
                    {photoPreview && (
                      <div className="mb-4">
                        <img
                          src={photoPreview}
                          alt="Preview"
                          className="w-full h-48 object-cover rounded-lg"
                        />
                      </div>
                    )}

                    <div className="space-y-2">
                      <button
                        onClick={() => document.getElementById('photoInput')?.click()}
                        className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg hover:bg-blue-600 transition font-medium"
                      >
                        📁 Выбрать файл
                      </button>

                      <button
                        onClick={() => setIsCameraOpen(true)}
                        className="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 transition font-medium"
                      >
                        📷 Сфотографировать
                      </button>
                    </div>

                    <input
                      id="photoInput"
                      type="file"
                      accept="image/*"
                      onChange={handlePhotoSelect}
                      className="hidden"
                    />

                    {photoFile && (
                      <p className="text-sm text-gray-600 mt-3">
                        ✓ {photoFile.name}
                      </p>
                    )}
                  </div>
                )}

                <div className="flex gap-2">
                  <button
                    onClick={currentCow ? handleUpdateCow : handleAddCow}
                    disabled={isLoading}
                    className="flex-1 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-medium"
                  >
                    {isLoading ? '⏳ Сохранение...' : '✓ Сохранить'}
                  </button>
                  <button
                    onClick={() => {
                      setShowForm(false);
                      if (!currentCow) {
                        setFormData({ name: '', breed: '', age: '', weight: '', insemination_status: false, insemination_date: '' });
                        setPhotoFile(null);
                        setPhotoPreview(null);
                      }
                    }}
                    className="flex-1 bg-gray-400 text-white py-2 px-4 rounded hover:bg-gray-500 transition font-medium"
                  >
                    ✕ Отмена
                  </button>
                </div>
              </div>
            </div>
          ) : showMedicalForm ? (
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold mb-4">Добавить медицинскую запись</h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold mb-2">Тип записи</label>
                  <select
                    name="record_type"
                    value={medicalData.record_type}
                    onChange={handleMedicalChange}
                    className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500"
                  >
                    <option value="vaccine">💉 Вакцинация</option>
                    <option value="disease">🦠 Болезнь</option>
                    <option value="treatment">💊 Лечение</option>
                    <option value="note">📝 Заметка</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Название *</label>
                  <input
                    type="text"
                    name="title"
                    value={medicalData.title}
                    onChange={handleMedicalChange}
                    className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-200"
                    placeholder="Например: Мастит"
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Описание</label>
                  <textarea
                    name="description"
                    value={medicalData.description}
                    onChange={handleMedicalChange}
                    className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500 focus:ring-1 focus:ring-green-200 h-20 resize-none"
                    placeholder="Дополнительная информация..."
                  />
                </div>

                <div>
                  <label className="block text-sm font-semibold mb-2">Дата</label>
                  <input
                    type="date"
                    name="record_date"
                    value={medicalData.record_date}
                    onChange={handleMedicalChange}
                    className="w-full border border-gray-300 rounded px-3 py-2"
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={handleAddMedicalRecord}
                    disabled={isLoading}
                    className="flex-1 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-medium"
                  >
                    {isLoading ? '⏳ Сохранение...' : '✓ Добавить'}
                  </button>
                  <button
                    onClick={() => setShowMedicalForm(false)}
                    className="flex-1 bg-gray-400 text-white py-2 px-4 rounded hover:bg-gray-500 transition font-medium"
                  >
                    ✕ Отмена
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg shadow-lg p-12 text-center text-gray-500">
              <p className="text-lg">Выберите корову из списка слева</p>
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

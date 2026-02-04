/**
 * Компонент для отображения медицинской карты коровы
 */

import React from 'react';

export default function MedicalCard({ cow }) {
  if (!cow) {
    return null;
  }

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('ru-RU');
  };

  const recordTypeLabels = {
    vaccine: '💉 Вакцинация',
    disease: '🦠 Болезнь',
    treatment: '💊 Лечение',
    note: '📝 Заметка'
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Заголовок с информацией коровы */}
      <div className="bg-gradient-to-r from-green-600 to-green-700 text-white p-6">
        <h2 className="text-3xl font-bold mb-2">{cow.name}</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-green-100 text-sm">Порода</p>
            <p className="text-lg font-semibold">{cow.breed}</p>
          </div>
          <div>
            <p className="text-green-100 text-sm">Возраст</p>
            <p className="text-lg font-semibold">{cow.age} лет</p>
          </div>
          {cow.weight && (
            <div>
              <p className="text-green-100 text-sm">Вес</p>
              <p className="text-lg font-semibold">{cow.weight} кг</p>
            </div>
          )}
          <div>
            <p className="text-green-100 text-sm">ID</p>
            <p className="text-lg font-semibold">#{cow.id}</p>
          </div>
        </div>
      </div>

      {/* Фото коровы */}
      {cow.photo_path && (
        <div className="p-6 bg-gray-50 border-b">
          <img
            src={`http://localhost:8000/${cow.photo_path}`}
            alt={cow.name}
            className="w-full h-48 object-cover rounded-lg"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/300x200?text=Cow';
            }}
          />
        </div>
      )}

      {/* Информация об осеменении */}
      <div className="p-6 border-b bg-gray-50">
        <h3 className="text-lg font-bold mb-3 flex items-center">
          <span className="mr-2">🔬</span>
          Осеменение
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600">Статус</p>
            <p className="text-xl font-semibold">
              {cow.insemination_status ? (
                <span className="text-green-600">✓ Да</span>
              ) : (
                <span className="text-gray-600">✗ Нет</span>
              )}
            </p>
          </div>
          {cow.insemination_date && (
            <div className="bg-white p-4 rounded-lg border border-gray-200">
              <p className="text-sm text-gray-600">Дата осеменения</p>
              <p className="text-xl font-semibold">
                {formatDate(cow.insemination_date)}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Медицинские записи */}
      <div className="p-6">
        <h3 className="text-2xl font-bold mb-4 flex items-center">
          <span className="mr-2">📋</span>
          Медицинская карта
        </h3>

        {cow.medical_records && cow.medical_records.length > 0 ? (
          <div className="space-y-3">
            {cow.medical_records.map((record) => (
              <div
                key={record.id}
                className="bg-gray-50 p-4 rounded-lg border-l-4 border-green-500"
              >
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-gray-800">
                    {recordTypeLabels[record.record_type] || record.record_type}
                  </p>
                  <p className="text-sm text-gray-500">
                    {formatDate(record.record_date)}
                  </p>
                </div>
                <p className="text-gray-700 font-semibold mb-1">{record.title}</p>
                {record.description && (
                  <p className="text-gray-600 text-sm">{record.description}</p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 text-center py-8">
            Медицинские записи отсутствуют
          </p>
        )}
      </div>

      {/* Footer */}
      <div className="bg-gray-50 px-6 py-4 border-t text-sm text-gray-600">
        <p>
          Создано: {formatDate(cow.created_at)}
        </p>
        {cow.updated_at !== cow.created_at && (
          <p>
            Обновлено: {formatDate(cow.updated_at)}
          </p>
        )}
      </div>
    </div>
  );
}

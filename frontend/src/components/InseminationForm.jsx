/**
 * Form component for managing cow insemination data
 */

import React, { useState, useEffect } from 'react';

export default function InseminationForm({ cow, onSave, onCancel, isLoading }) {
  const [inseminationStatus, setInseminationStatus] = useState(false);
  const [inseminationDate, setInseminationDate] = useState('');

  useEffect(() => {
    if (cow) {
      setInseminationStatus(cow.insemination_status || false);
      setInseminationDate(
        cow.insemination_date ? cow.insemination_date.split('T')[0] : ''
      );
    }
  }, [cow]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      insemination_status: inseminationStatus,
      insemination_date: inseminationDate ? new Date(inseminationDate).toISOString() : null
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-4">🔬 Управление осеменением</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold mb-3">
            <input
              type="checkbox"
              checked={inseminationStatus}
              onChange={(e) => setInseminationStatus(e.target.checked)}
              className="w-4 h-4 rounded"
            />
            <span className="ml-2">Осеменена</span>
          </label>
        </div>

        {inseminationStatus && (
          <div>
            <label className="block text-sm font-semibold mb-2">
              Дата осеменения
            </label>
            <input
              type="date"
              value={inseminationDate}
              onChange={(e) => setInseminationDate(e.target.value)}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-green-500"
            />
          </div>
        )}

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={isLoading}
            className="flex-1 bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-medium"
          >
            {isLoading ? '⏳ Сохранение...' : '✓ Сохранить'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 bg-gray-400 text-white py-2 px-4 rounded hover:bg-gray-500 transition font-medium"
          >
            ✕ Отмена
          </button>
        </div>
      </form>
    </div>
  );
}

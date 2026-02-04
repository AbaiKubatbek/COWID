/**
 * API клиент для взаимодействия с Backend
 * Использует Axios для HTTP запросов
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Создаём Axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// ========== COWS API ==========

/**
 * Получить все коов
 */
export const getCows = async () => {
  try {
    const response = await apiClient.get('/cows');
    return response.data;
  } catch (error) {
    console.error('Ошибка при получении коов:', error);
    throw error;
  }
};

/**
 * Получить конкретную корову
 */
export const getCow = async (cowId) => {
  try {
    const response = await apiClient.get(`/cows/${cowId}`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при получении коовы ${cowId}:`, error);
    throw error;
  }
};

/**
 * Создать новую корову
 */
export const createCow = async (cowData, photoFile) => {
  try {
    const formData = new FormData();
    
    // Добавляем поля данных коровы как отдельные поля формы
    formData.append('name', cowData.name);
    formData.append('breed', cowData.breed);
    formData.append('age', cowData.age);
    if (cowData.weight) {
      formData.append('weight', cowData.weight);
    }
    
    // Добавляем файл фото если есть
    if (photoFile) {
      formData.append('photo', photoFile);
    }
    
    const response = await apiClient.post('/cows', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при создании коовы:', error);
    throw error;
  }
};

/**
 * Обновить коову
 */
export const updateCow = async (cowId, cowData) => {
  try {
    const response = await apiClient.put(`/cows/${cowId}`, cowData);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при обновлении коовы ${cowId}:`, error);
    throw error;
  }
};

/**
 * Удалить корову
 */
export const deleteCow = async (cowId) => {
  try {
    const response = await apiClient.delete(`/cows/${cowId}`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при удалении коовы ${cowId}:`, error);
    throw error;
  }
};

// ========== MEDICAL RECORDS API ==========

/**
 * Получить медицинские записи коовы
 */
export const getMedicalRecords = async (cowId) => {
  try {
    const response = await apiClient.get(`/cows/${cowId}/medical-records`);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при получении медицинских записей:`, error);
    throw error;
  }
};

/**
 * Добавить медицинскую запись
 */
export const addMedicalRecord = async (cowId, recordData) => {
  try {
    const response = await apiClient.post(`/cows/${cowId}/medical-records`, recordData);
    return response.data;
  } catch (error) {
    console.error(`Ошибка при добавлении медицинской записи:`, error);
    throw error;
  }
};

// ========== RECOGNITION API ==========

/**
 * Распознать корову по фото
 */
export const recognizeFromImage = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await apiClient.post('/recognize/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при распознавании:', error);
    throw error;
  }
};

/**
 * Получить debug информацию о распознавании
 */
export const recognizeWithDebug = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('image', imageFile);
    
    const response = await apiClient.post('/recognize/debug', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
    return response.data;
  } catch (error) {
    console.error('Ошибка при debug распознавании:', error);
    throw error;
  }
};

/**
 * WebSocket для видеопотока
 */
export const connectVideoStream = (onMessage, onError) => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host.replace(':3000', ':8000')}/api/recognize/stream`;
  
  const ws = new WebSocket(wsUrl);
  
  ws.onopen = () => {
    console.log('WebSocket соединение установлено');
  };
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onMessage(data);
    } catch (error) {
      console.error('Ошибка при парсинге WebSocket сообщения:', error);
    }
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket ошибка:', error);
    if (onError) {
      onError(error);
    }
  };
  
  return ws;
};

export default apiClient;

# CowID Frontend

## 📋 Описание

React frontend для системы распознавания лиц коров. Предоставляет интуитивный интерфейс для распознавания коров, управления их данными и просмотра медицинских карт.

## 🚀 Быстрый старт

### 1. Установка

```bash
cd frontend
npm install
```

### 2. Запуск в development режиме

```bash
npm run dev
```

Приложение будет доступно на `http://localhost:3000`

### 3. Build для production

```bash
npm run build
```

## 📁 Структура проекта

```
frontend/src/
├── main.jsx                      # Entry point
├── App.jsx                       # Главный компонент
├── index.css                     # Tailwind стили
├── components/
│   ├── AdminPanel.jsx           # Admin панель (CRUD)
│   ├── RecognitionForm.jsx      # Распознавание по фото
│   ├── VideoCapture.jsx         # Видеопоток (не включен в основную версию)
│   └── MedicalCard.jsx          # Карточка с медицинской информацией
├── pages/
│   ├── AdminPage.jsx
│   ├── RecognitionPage.jsx
│   └── HomePage.jsx
├── services/
│   └── api.js                   # API клиент (Axios)
└── store/
    └── store.js                 # Zustand state management
```

## 🎨 UI Components

### AdminPanel
Полнофункциональная админ-панель для управления коовами:
- **Список коов** - Выбор коовы из списка
- **Форма создания** - Добавление новой коовы с фото
- **Форма редактирования** - Изменение данных коовы
- **Медицинские записи** - Добавление записей о вакцинациях, болезнях и т.д.
- **Удаление** - Безопасное удаление коовы

### RecognitionForm
Загрузка фото и распознавание коовы:
- **Выбор файла** - Интуитивный интерфейс для загрузки
- **Preview** - Просмотр выбранного изображения
- **Результат** - Информация о распознанной корове
- **Медкарта** - Полная информация о корове

### MedicalCard
Отображение информации о корове:
- Основные данные (имя, порода, возраст)
- Фото морды
- История медицинских записей

## 🔧 API Integration

### Основные endpoints

```javascript
// Управление коовами
GET /api/cows                          // Все коовы
POST /api/cows                         // Создать корову
GET /api/cows/{id}                     // Одна коова
PUT /api/cows/{id}                     // Обновить
DELETE /api/cows/{id}                  // Удалить

// Медицинские записи
GET /api/cows/{id}/medical-records     // История
POST /api/cows/{id}/medical-records    // Добавить запись

// Распознавание
POST /api/recognize/image              // Распознать по фото
WS /api/recognize/stream               // Видеопоток (WebSocket)
```

## 📦 Зависимости

- **React 18** - UI библиотека
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP клиент
- **Zustand** - State management
- **React Router** - Маршрутизация (опционально)

## 🎯 Features

### Распознавание
- ✅ Загрузка изображения
- ✅ Отправка на backend
- ✅ Вывод результатов
- ⏳ Видеопоток (в разработке)

### Admin панель
- ✅ Список всех коов
- ✅ Создание новой коовы
- ✅ Редактирование данных
- ✅ Управление медицинскими записями
- ✅ Удаление коов

### Медицинская карта
- ✅ Основная информация
- ✅ История вакцинаций
- ✅ История болезней
- ✅ История лечений
- ✅ Дополнительные заметки

## 🔌 API клиент

### Использование

```javascript
import { getCows, recognizeFromImage, createCow } from './services/api';

// Получить всех коов
const cows = await getCows();

// Распознать по фото
const result = await recognizeFromImage(imageFile);

// Создать новую корову
const newCow = await createCow({
  name: 'Bessie',
  breed: 'Holstein',
  age: 5,
  weight: 600
}, photoFile);
```

## 📊 State Management (Zustand)

### Cows Store
```javascript
const { cows, currentCow, setCows, setCurrentCow } = useCowStore();
```

### Recognition Store
```javascript
const { recognitionResult, setRecognitionResult } = useRecognitionStore();
```

### UI Store
```javascript
const { currentPage, setCurrentPage } = useUIStore();
```

## 🎨 Tailwind CSS

Все стили используют Tailwind CSS:
- Responsive дизайн
- Dark mode support (опционально)
- Custom components

## 📱 Responsive Design

- Mobile-first подход
- Оптимизирован для всех экранов
- Touch-friendly интерфейс

## 🚀 Production Build

```bash
npm run build
```

Создаёт оптимизированный build в папке `dist/`

### Развертывание

```bash
# Static hosting (Netlify, Vercel, etc)
npm run build
# Загрузить папку dist

# Docker
docker build -t cowid-frontend .
docker run -p 80:3000 cowid-frontend
```

## 🔒 Security

- ✅ CORS обработана в backend
- ✅ Input валидация
- ✅ Error handling

## 🐛 Дебаг

Включены console.log'и для дебага:
- API запросы
- State обновления
- Ошибки

Отключите их перед production build'ом в `services/api.js`

## 🤝 Улучшения

### Будущие features
- [ ] Видеопоток в реальном времени
- [ ] Экспорт медицинских данных (PDF)
- [ ] Графики производительности коов
- [ ] Система уведомлений
- [ ] Темная тема
- [ ] Multi-язычность

## 📝 Лицензия

MIT License

# 🚀 БЫСТРЫЙ СТАРТ - CowID

## ⚡ Запуск в 1 команду (Docker)

```bash
docker-compose up
```

Затем откройте:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔧 Запуск без Docker (Локально)

### Требования
- Python 3.9+
- Node.js 16+
- Git

### Шаг 1: Запуск Backend

```bash
# Перейти в папку backend
cd backend

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить Backend
python -m uvicorn app.main:app --reload
```

Backend будет на: **http://localhost:8000**

### Шаг 2: Запуск Frontend (новый Terminal)

```bash
# Перейти в папку frontend
cd frontend

# Установить зависимости
npm install

# Запустить Frontend
npm run dev
```

Frontend будет на: **http://localhost:3000**

---

## 📚 Документация

После запуска, прочитайте:

1. **[README.md](./README.md)** ⭐ - Главное описание проекта
2. **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Архитектура системы
3. **[FILE_STRUCTURE.md](./FILE_STRUCTURE.md)** - Структура файлов
4. **[INSTALL.md](./INSTALL.md)** - Полное руководство установки
5. **[EXAMPLES.py](./EXAMPLES.py)** - Примеры использования API

---

## 🎯 Первые шаги в приложении

### 1. Добавить новую корову

1. Откройте http://localhost:3000
2. Нажмите **"⚙️ Admin"** в меню
3. Нажмите **"+ Добавить"**
4. Заполните данные:
   - **Имя**: Bessie
   - **Порода**: Holstein
   - **Возраст**: 5
5. Загрузите **фото морды** коровы
6. Нажмите **"✓ Сохранить"**

### 2. Распознать корову

1. Нажмите **"🔍 Распознавание"** в меню
2. Загрузите фото той же коровы
3. Нажмите **"🔍 Распознать"**
4. Вы увидите медицинскую карту коровы!

### 3. Добавить медицинскую запись

1. В Admin панели выберите корову из списка
2. Нажмите **"➕ Медзапись"**
3. Выберите тип (вакцина, болезнь, и т.д.)
4. Заполните информацию
5. Нажмите **"✓ Добавить"**

---

## 🔌 API примеры

### Получить всех коов

```bash
curl http://localhost:8000/api/cows
```

### Распознать по фото

```bash
curl -X POST http://localhost:8000/api/recognize/image \
  -F "image=@cow_photo.jpg"
```

### Создать новую корову

```bash
curl -X POST http://localhost:8000/api/cows \
  -F 'cow_data={"name":"Bessie","breed":"Holstein","age":5}' \
  -F "photo=@photo.jpg"
```

Полная API документация на: http://localhost:8000/docs

---

## 📁 Основные файлы

| Файл | Описание |
|------|---------|
| [backend/app/main.py](./backend/app/main.py) | FastAPI приложение |
| [backend/app/api/cows.py](./backend/app/api/cows.py) | CRUD операции |
| [backend/app/api/recognize.py](./backend/app/api/recognize.py) | Распознавание |
| [backend/app/ml_models/](./backend/app/ml_models/) | ML модели (YOLOv8, ResNet50) |
| [frontend/src/App.jsx](./frontend/src/App.jsx) | Главный React компонент |
| [frontend/src/components/](./frontend/src/components/) | React компоненты |
| [frontend/src/services/api.js](./frontend/src/services/api.js) | API клиент |

---

## 🐛 Проблемы?

### Backend не запускается

```bash
# Проверить Python версию
python --version

# Переустановить зависимости
pip install -r requirements.txt --force-reinstall

# Проверить что порт 8000 свободен
netstat -ano | findstr :8000
```

### Frontend ошибка подключения

```bash
# Проверить что Backend запущен
curl http://localhost:8000/health

# Очистить npm кэш
npm cache clean --force
npm install
```

### Database ошибка

```bash
# Для SQLite - удалить и пересоздать
rm cows.db

# Потом перезапустить Backend
```

---

## 🎓 Обучение

### Для новичков
1. Читайте комментарии в коде (на русском)
2. Смотрите примеры в [EXAMPLES.py](./EXAMPLES.py)
3. Изучите [ARCHITECTURE.md](./ARCHITECTURE.md)

### Для опытных
1. ML pipeline находится в `backend/app/ml_models/`
2. API endpoints в `backend/app/api/`
3. Frontend компоненты в `frontend/src/components/`
4. State management в `frontend/src/store/`

---

## 📊 Technology Stack

### Backend
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **PyTorch** - глубокое обучение
- **OpenCV** - обработка изображений
- **YOLOv8** - детекция объектов
- **ResNet50** - извлечение признаков

### Frontend
- **React 18** - UI библиотека
- **Vite** - fast build tool
- **Tailwind CSS** - стили
- **Axios** - HTTP клиент
- **Zustand** - state management

### Database
- **SQLite** (development)
- **PostgreSQL** (production)

---

## 🚀 Production Deploy

### С Docker

```bash
docker-compose -f docker-compose.yml up -d
```

### На сервер

```bash
# Backend
pip install gunicorn
gunicorn -w 4 app.main:app

# Frontend
npm run build
npm install -g serve
serve -s dist
```

---

## 📞 Дополнительная помощь

- 📖 **README.md** - Полное описание проекта
- 🏗️ **ARCHITECTURE.md** - Архитектура системы
- 📋 **FILE_STRUCTURE.md** - Структура файлов
- 📚 **INSTALL.md** - Полное руководство установки
- 💻 **EXAMPLES.py** - Примеры кода
- 📖 **Backend README** - `backend/README.md`
- 📖 **Frontend README** - `frontend/README.md`

---

## ✅ Checklist для первого запуска

- [ ] Docker установлен или Python + Node.js готовы
- [ ] Склонирован/скопирован репозиторий
- [ ] Выполнена команда `docker-compose up` или локальный setup
- [ ] Frontend открывается на http://localhost:3000
- [ ] Backend API доступен на http://localhost:8000
- [ ] API документация на http://localhost:8000/docs
- [ ] Добавлена первая коова в Admin панели
- [ ] Коова успешно распознана по фото

---

## 🎉 Готово!

Вы готовы использовать **CowID** для распознавания и управления коровами!

**Приятного использования! 🐄**

---

<div align="center">
  <p><strong>CowID v1.0</strong> - Система интеллектуального распознавания лиц коров</p>
  <p>Сделано с ❤️ для животноводства</p>
</div>

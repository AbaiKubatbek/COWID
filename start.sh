#!/bin/bash
# Скрипт для быстрого запуска CowID в development режиме

echo "🐄 CowID - Запуск в development режиме"
echo "======================================="

# Проверка наличия Docker
if command -v docker &> /dev/null; then
    echo ""
    echo "📦 Docker найден! Используем Docker Compose..."
    echo ""
    docker-compose up
    exit 0
fi

# Если Docker не установлен, запускаем локально
echo ""
echo "❌ Docker не найден. Запуск локально..."
echo ""

# Проверка Python
if ! command -v python &> /dev/null; then
    echo "❌ Python не найден! Установите Python 3.9+"
    exit 1
fi

# Проверка Node.js
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js не найден! Установите Node.js 16+"
    exit 1
fi

echo "✅ Python и Node.js найдены"
echo ""

# Запуск Backend в фоне
echo "🚀 Запуск Backend на порту 8000..."
cd backend
python -m venv venv
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    venv\Scripts\activate
else
    source venv/bin/activate
fi
pip install -r requirements.txt > /dev/null 2>&1
python -m uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

echo "🎨 Запуск Frontend на порту 3000..."
cd frontend
npm install > /dev/null 2>&1
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "======================================="
echo "✅ CowID запущен!"
echo "======================================="
echo ""
echo "📍 Frontend: http://localhost:3000"
echo "📍 Backend:  http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
echo ""
echo "Нажмите Ctrl+C для остановки"
echo ""

# Ждём сигнала Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT
wait

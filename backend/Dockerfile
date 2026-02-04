# Backend Docker
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей для OpenCV
RUN apt-get update && apt-get install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY backend/app ./app

# Создаём папку для uploads
RUN mkdir -p uploads

# Expose port
EXPOSE 8000

# Start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend Docker
FROM node:18-alpine

WORKDIR /app

# Копируем package files
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем исходный код
COPY . .

# Build приложения
RUN npm run build

# Используем простой HTTP сервер
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=0 /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]

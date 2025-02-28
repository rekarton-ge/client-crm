FROM node:18-alpine

WORKDIR /app

# Копируем сначала только файлы зависимостей
COPY package.json ./
# Используем install вместо ci
RUN npm install

# Копируем остальные файлы
COPY . .

# Start development server
CMD ["npm", "start"]
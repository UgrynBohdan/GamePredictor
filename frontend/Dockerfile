# --- ЕТАП 1: ЗБІРКА ЗАСТОСУНКУ REACT ---
# Використовуємо офіційний образ Node.js на базі Alpine для збірки
FROM node:lts-alpine as build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

# --- ЕТАП 2: РОЗГОРТАННЯ ЗІБРАНОГО ЗАСТОСУНКУ ЗА ДОПОМОГОЮ NGINX ---
# Використовуємо легкий офіційний образ Nginx на базі Alpine
FROM nginx:alpine as production-stage

# Копіюємо зібрані статичні файли з build-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80

# Команда для запуску Nginx
CMD ["nginx", "-g", "daemon off;"]


# build stage
FROM node:12.14.0-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM nginx:1.16.1-alpine as production-stage
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf 
# 삭제 해야할지도 모름

COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD [ "nginx", "-g", "daemon off;"]

# Netflix at Home — Frontend

Фронтенд для онлайн-кинотеатра на **Angular (standalone)**:  
- страница авторизации/регистрации  
- главная страница со списком фильмов и поиском  
- страница фильма (детали)  
- страница плеера  
- отправка метрик в сервис `nx_metrics` (порт `8900`)

## Требования

- **Node.js** (желательно LTS https://nodejs.org/en/download)
- **npm**
- **Angular CLI** (npm i -g @angular/cli)

Проверка версий:
```bash
node -v
npm -v
```
Установка зависимостей в корне фронтенда:
```bash
npm install
```
Запуск локально:
```bash
ng serve
```
По умолчанию приложение откроется:
http://localhost:4200

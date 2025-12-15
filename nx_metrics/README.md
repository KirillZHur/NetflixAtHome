# Сервис сбора метрик

Доступен на ```localhost:8900```.

## Метрики по фильмам

Типы метрик:
- film_visited - пользователь посетил страницу фильма;
- start_watching_film - пользователь начал просмотр фильма;
- finished_watching_film - пользователь завершил просмотр фильма.

Пример запроса 
```
POST  http://localhost:8900/film_event
HEADERS:
    "Authorization": {User JWT} 
BODY:
{
    "film_id": "1be431f1-a85a-4ebe-b62d-1015bf89dfe1",
    "film_event_tag": "film_visited",
    "event_time": "2025-12-14 09:09:09"
}
```

## Метрики по пользователям

Типы метрик:
- user_registered - пользователь зарегистрировался на платформе;
- user_login - пользователь зашел на сайт.

Пример запроса 
```
POST  http://localhost:8900/user_event
HEADERS:
    "Authorization": {User JWT} 
BODY:
{
    "user_event_tag": "site_opened",
    "event_time": "2025-12-14 09:09:09"
}
```

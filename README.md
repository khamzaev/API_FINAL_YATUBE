# API_FINAL_YATUBE

## Описание

API_FINAL_YATUBE - это API для платформы блогов, позволяющее пользователям создавать и управлять публикациями, комментариями и подписками на других пользователей. Проект решает задачу предоставления удобного интерфейса для работы с контентом и взаимодействия с другими пользователями через API. API поддерживает аутентификацию с использованием JWT-токенов для обеспечения безопасности и контроля доступа.

## Установка

Следуйте этим инструкциям, чтобы развернуть проект на локальной машине.

### Клонирование репозитория

```sh
git clone https://github.com/khamzaev/API_FINAL_YATUBE.git
cd API_FINAL_YATUBE
```

### Создание виртуального окружения

```sh
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
```

### Установка зависимостей

```sh
pip install -r requirements.txt
```

### Применение миграций

```sh
python manage.py migrate
```

### Создание суперпользователя

```sh
python manage.py createsuperuser
```

### Запуск сервера разработки

```sh
python manage.py runserver
```

Теперь проект доступен по адресу `http://127.0.0.1:8000/`.

## Примеры запросов к API

### Получение списка публикаций

```http
GET /api/v1/posts/
```

Пример ответа:

```json
{
    "count": 123,
    "next": "http://api.example.org/posts/?offset=20&limit=10",
    "previous": "http://api.example.org/posts/?offset=0&limit=10",
    "results": [
        {
            "id": 1,
            "author": "user1",
            "text": "Первая публикация",
            "pub_date": "2025-03-09T14:00:00Z",
            "image": null,
            "group": 1
        },
        ...
    ]
}
```

### Создание новой публикации

```http
POST /api/v1/posts/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "text": "Новая публикация",
    "image": null,
    "group": 1
}
```

Пример ответа:

```json
{
    "id": 124,
    "author": "user1",
    "text": "Новая публикация",
    "pub_date": "2025-03-09T14:10:00Z",
    "image": null,
    "group": 1
}
```

### Получение списка комментариев к публикации

```http
GET /api/v1/posts/1/comments/
```

Пример ответа:

```json
[
    {
        "id": 1,
        "author": "user2",
        "text": "Отличная публикация!",
        "created": "2025-03-09T14:15:00Z",
        "post": 1
    },
    ...
]
```

### Подписка на пользователя

```http
POST /api/v1/follow/
Authorization: Bearer <your_token>
Content-Type: application/json

{
    "following": "user2"
}
```

Пример ответа:

```json
{
    "user": "user1",
    "following": "user2"
}
```

### Получение списка подписок

```http
GET /api/v1/follow/
Authorization: Bearer <your_token>
```

Пример ответа:

```json
[
    {
        "user": "user1",
        "following": "user2"
    },
    ...
]
```
### Автор Проекта

Джамал Хамзаев

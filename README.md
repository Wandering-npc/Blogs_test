# Blogs_test

## Тестовое задание backend #1 (REST API Python)

### Описание

Реализация REST API для социальной платформы блогов с использованием Python и Django.

### Основные возможности

- Создание пользователей и персональных блогов при их создании.
- Создание и управление постами в блоге (заголовок, текст, время создания).
- Подписка и отписка пользователей от блогов других пользователей.
- Персональная лента новостей пользователя, содержащая посты из блогов, на которые он подписан, с пагинацией.
- Пометка постов в ленте как прочитанных.
- Отправка подборки последних постов ленты на почту раз в сутки.

### Требования

- Python 3.x
- Django > 4.x + DRF или FastAPI
- PostgreSQL
- Celery и Redis (опционально)
- Docker и docker-compose

### Дополнительно

- Код проекта должен быть доступен на GitHub и отражать процесс разработки с несколькими коммитами.
- Проект должен быть упакован в Docker и запускаться через `docker-compose`.
- README должен содержать описание проекта и инструкции по запуску.

### Установка и запуск проекта

1. Создайте файл `.env` (пример находится в репозитории).

2. Соберите сеть контейнеров:

    ```bash
    docker-compose up
    ```

3. Запустите миграции:

    ```shell
    docker compose exec web python manage.py migrate
    ```

4. Создайте суперпользователя:

    ```shell
    docker compose exec web python manage.py createsuperuser
    ```

5. Запустите команду для генерации постов:

    ```shell
    docker compose exec web python manage.py generate_posts
    ```

### API Endpoints

- Получение токена: `POST /api/auth/token/login/`
- Получение списка пользователей: `GET /api/v1/users/`
- Подписка/отписка на пользователя: `POST /api/v1/users/<user_id>/subscribe/` и `DELETE /api/v1/users/<user_id>/subscribe/`
- Получение персональной ленты пользователя: `POST /api/v1/posts/?page=<page_id>` или `POST /api/v1/posts/`
- Отметка поста как прочитанного/непрочитанного: `POST /api/v1/posts/<post_id>/mark_as_read/` и `DELETE /api/v1/posts/<post_id>/mark_as_read/`
- Получение списка блогов: `GET /api/v1/blogs/`
- Получение блога с постами: `GET /api/v1/blogs/<blog_id>`


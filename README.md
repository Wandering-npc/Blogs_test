# Blogs_test
## Тестовое задание backend #1 (rest api Python)
### Текст задания
_Реализовать rest api:_
Имеется база пользователей (добавляются через админку/swagger, регистрацию делать не надо).
У каждого пользователя при создании создается персональный блог. Новые создавать он не может.
Пост в блоге — элементарная запись с заголовком, текстом (140 символов) и временем создания. Заголовок обязательное поле.
Пользователь может подписываться/отписываться на блоги других пользователей (любое количество).
У пользователя есть персональная лента новостей (не более ~500 постов), в которой выводятся посты из блогов, на которые он подписан, в порядке добавления постов. Пагинация по 10 постов.
Пользователь может помечать посты в ленте прочитанными.
При удалении/добавлении поста, лента тоже должна изменяться
Раз в сутки на почту прилетает подборка из 5 последних постов ленты (можно в консоль)
В среднем пользователь подписан на 100 человек, которые постят по 2-3 раза в день.
Предполагаемое кол-во пользователей в системе около 1 млн.
Будет плюсом:
Если добавить дамп с большим кол-вом записей или добавить команду, которая сама генерирует большой объем данных.
Можно использовать - https://mixer.readthedocs.io/en/latest/api.html - https://stackoverflow.com/questions/36463134/generate-test-data-in-postgresql-table
Будет плюсом наличие тестов.
Требования:
Python 3.x, Django > 4.х + Drf или FastApi, Postgresql. Можно использовать Celery и Redis.
Проект должен быть на гитхабе и отражать процесс разработки. НЕ один коммит на всё.
Код максимально приближенный к боевому (насколько получится).
Проект необходимо упаковать в докер. Запускать через docker-compose.
В проекте должно быть README с описанием запуска проекта.


## Запуск проекта

1) Собираем сеть контейнеров:
```bash
docker-compose up
```
2) Запускаем миграции:
```shell
docker compose exec web  python manage.py migrate
```
3) Создаем суперюзера:
```shell
docker compose exec web python manage.py createsuperuser
```
4) Запускаем менеджмент команду для генерации постов
```shell
docker compose exec web python manage.py generate_posts
```
<br><br>
## Deploy
1) Выдать права на запуск данных скриптов: 
```shell
chmod +x ./blog/entrypoint.sh && chmod +x ./blog/entrypoint.prod.sh
```
2) Создать образ и запустить контейнер в фоне:
```shell
docker-compose -f docker-compose.yml up -d --build
```
3) Выполнить миграции
```shell
docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput
```
4) Сборка стандартных и подготовленных статических файлов 
```shell
docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input --clear
```
5) Заполнить таблицы подготовленными данными. `3-4` можно пропустить - сразу запустить этот пункт
```shell
docker-compose -f docker-compose.yml exec web python manage.py fill_db
```

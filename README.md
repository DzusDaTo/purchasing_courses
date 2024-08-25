# REST API для Fiagdon app


## В приложении реализованы следующие концепции:
- Разработка Веб-Приложений на Python[DjangoRestFramework], следуя дизайну REST API.
- Подход Чистой Архитектуры в построении структуры приложения. Техника внедрения зависимости.
- Работа с БД Postgres. Генерация файлов миграций. Обращение через ORM.
- Работа с БД Redis. Кэширование. 
- Работа с Celery. Отправка уведомлений о завершении курса.


#### Создаем виртуальное окружение
```
python3 -m venv .venv && source .venv/bin/activate
```

#### Устаналиваем зависимости
```
pip install -r requirements.txt
```

#### Подготавливаем БД и заполняем данными
```
./manage.py migrate

```
```
./manage.py loaddata fixtures/categories.json fixtures/cottages.json fixtures/likes.json fixtures/rents.json fixtures/reviews.json  fixtures/towns.json fixtures/users.json fixtures/chats.json fixtures/messages.json

```

#### Для запуска тестов:
```
coverage run manage.py test && coverage report
```

### Docker:

```
docker-compose build
```

```

## Инструкция

### Задача: спроектировать и разработать API для системы опросов пользователей.

Использовать следующие технологии: Django 2.2.10, Django REST framework.

#### Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения в docker
- документация по API


### Документация:


#### структура

- app/build - необходимые для развертывания приложения настройки (requirements)
- dev/docker - файлы докера и переменные окружения
- app/src - исходный код приложения


#### Используется:
#### - python:3.10
#### - PostgresSQL 14.1

### Requirements:
- Django==2.2.10
- djangorestframework==3.11.0
- psycopg2-binary==2.9.3
- django-debug-toolbar==3.2.4
- django-debug-toolbar-force==0.1.8
- coverage==6.2
- drf-yasg==1.17.1


### Документация API SWAGGER
```djangourlpath
JSON  /swagger.json
YAML  /swagger.yaml
swagger-ui  /swagger/
```

## Запуск приложения в Docker (должен быть установлен)

В папке dev/docker переименовать .env.tmpl в .env и описать в нем необходимые переменные окружения

### Запустите тесты:
```shell
docker-compose run web ./manage.py test
```

### Создание супер пользователя

```shell
docker-compose run web ./manage.py createsuperuser
```

### Запустите сервер:

```shell
docker-compose up
```

### Панель администратора:
```djangourlpath
/admin/
```


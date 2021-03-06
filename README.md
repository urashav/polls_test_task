## Инструкция

### Задача: спроектировать и разработать API для системы опросов пользователей.

#### Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

#### Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

#### Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API


#### Используется:
#### - Python 3.9
#### - PostgreSQL 14.1

### Requirements:
- Django==2.2.10
- djangorestframework==3.11.0
- psycopg2-binary==2.9.3
- django-debug-toolbar==3.2.4
- django-debug-toolbar-force==0.1.8
- coverage==6.2
- drf-yasg==1.17.1

Склонируйте git репозиторий:
```shell
mkdir project_name && cd project_name
git clone https://github.com/urashav/polls_test_task.git
cd polls_test_task
```

## Запуск приложения локально.

Внимание! Для локального запуска требутся PostgreSQL


Создайте виртуальное окружение:

```shell
python3 -m venv venv
```

Активируйте виртульное окружение:
```shell
source venv/bin/activate
```

Установите зависимости:
```shell
pip install -r requirements.txt
```


#### Создайте пользователя без пароля:
```shell
createuser db_username
```

#### Или создайте пользователя с паролем:
```shell
createuser db_username -P
```

#### Создайте базу данных:
```shell
createdb db_name -Odb_username
```

Для запуска тестов пользователь должен обладать правами на создание БД

#### Переопределите права пользователя:

Войдите в базу данных:
```shell
psql db_name
```

Введите команду:
```
ALTER USER username CREATEDB;
```

### Файл env_example.sh

Определит переменные окружения для приложения.
- Отредактируйте файл и введите актуальные настройки базы данных.
- Укажите любой SECRET_KEY.
- Переименуйте файл для удобства.

SECRET_KEY Можно сгенерировать в терминале:

```shell
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

#### Импортируйте переменные окружения из файла в терминале:

```shell
source env.sh
```

### Выполните команду миграций
```shell
python manage.py migrate
```
Если миграции прошли успешно, все настроено правильно

### Запустите тесты:
```shell
python manage.py test
```

### Создайте супер пользователя
```shell
python manage.py createsuperuser
```

### Запустите сервер Django
```shell
python manage.py runserver
```

## Запуск приложения в Docker (должен быть установлен)

#### В приложении имеется Makefile с сокращенными командами:

```makefile
up:
	docker-compose up
down:
	docker-compose down
test:
	docker-compose run web ./manage.py test
makemigrations:
	docker-compose run web ./manage.py makemigrations
migrate:
	docker-compose run web ./manage.py migrate
createsuperuser:
	docker-compose run web ./manage.py createsuperuser
```

#### Запуск команды
```shell
make <command>
```


### Соберите приложение:
```shell
docker-compose build
```

### Выполните команду миграций:

```shell
docker-compose run web ./manage.py migrate
```

### Запустите тесты:
```shell
docker-compose run web ./manage.py test
```

### Создание супер пользвателя

```shell
docker-compose run web ./manage.py createsuperuser
```

### Запустите сервер:

```shell
docker-compose up
```

### Остановить сервер (Ctrl+C):

```shell
docker-compose down
```

### Панель администратора:
```djangourlpath
/admin/
```

### Документация API SWAGGER
```djangourlpath
JSON  /swagger.json
YAML  /swagger.yaml
A swagger-ui  /swagger/
```
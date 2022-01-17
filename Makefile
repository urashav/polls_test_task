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

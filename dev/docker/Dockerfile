FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ADD --chown=www-data:www-data app/_build/pip/ /var/app/build/pip/
RUN pip install -r /var/app/build/pip/dev_requirements.txt

VOLUME /var/app
EXPOSE 8000
WORKDIR /var/app/src

ADD --chown=www-data:www-data dev/docker/docker-entrypoint.sh /

CMD ["sh", "/docker-entrypoint.sh"]

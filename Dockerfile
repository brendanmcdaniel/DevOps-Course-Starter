FROM python:3.7-slim-buster as base
RUN apt-get update \
&& apt-get install -y curl \
&& curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
COPY ./todo-app ./todo-app 
EXPOSE 5000

FROM base as production
ENTRYPOINT cd ./todo-app/ && poetry install && poetry run gunicorn --bind 0.0.0.0:5000 wsgi:app

FROM base as development
ENTRYPOINT cd ./todo-app/ && poetry install && poetry run flask run --host 0.0.0.0
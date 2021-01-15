FROM python:3.7-slim-buster as base
COPY app.py .
COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .
COPY session_items.py .
COPY trello.py .
COPY wsgi.py .
COPY templates/ ./templates/
COPY .env .
COPY flask_config.py .
RUN apt-get update \
&& apt-get install -y \
build-essential \
libssl-dev \
zlib1g-dev \
libbz2-dev \
libreadline-dev \
libsqlite3-dev \
wget \
curl \
llvm \
libncurses5-dev \
libncursesw5-dev \
xz-utils \
tk-dev \
libffi-dev \
liblzma-dev \
python-openssl \
git \
gunicorn \
&& curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
ENV TRELLO_KEY=d90a23616310b352929cc25d4b8994e2
ENV TRELLO_TOKEN=6544c9da5fa9df0225a43f3342fdc4b4a769d87e419874765c6db394a72b9e67
RUN poetry install 
EXPOSE 5000
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:5000 wsgi:app
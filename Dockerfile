FROM python:3.7-slim-buster as base
COPY . .
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
RUN poetry install 
EXPOSE 5000
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0:5000 wsgi:app
FROM python:3.11.3-alpine

RUN apk add --no-cache ffmpeg
RUN apk add --no-cache build-base gcc libffi-dev g++ && \
    pip install poetry && \
    apk del build-base gcc libffi-dev g++

WORKDIR /app

COPY poetry.lock pyproject.toml /

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction

COPY . .

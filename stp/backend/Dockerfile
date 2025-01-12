# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY src/pyproject.toml src/poetry.lock* /app/src/

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --without dev

COPY ./src /app/src

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "collectstatic", "--noinput"]
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
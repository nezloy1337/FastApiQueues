# --- Этап 1: Base ---
FROM python:3.13-slim  AS base

# Обновляем пакеты, устанавливаем curl и очищаем кэш
RUN apt-get update \
  && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean

# --- Этап 2: Export зависимостей из Poetry ---
FROM base AS poetry-export

# Задаём переменные окружения: добавляем путь к Poetry и указываем версию
ENV PATH=$PATH:/root/.local/bin \
    POETRY_VERSION=1.8.3

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python - --version $POETRY_VERSION

# Копируем файлы конфигурации Poetry (они должны находиться в корне проекта)
COPY pyproject.toml poetry.lock ./

# Экспортируем зависимости из группы main в requirements.txt (без хешей)
RUN poetry export --no-interaction -o /requirements.txt --without-hashes --only main

# --- Этап 3: Установка зависимостей через pip ---
FROM base AS requirements

# Устанавливаем необходимые инструменты для сборки (например, gcc и python3-dev)
RUN apt-get update && apt-get install -y gcc python3-dev --no-install-recommends && apt-get clean

# Копируем экспортированный requirements.txt из этапа poetry-export
COPY --from=poetry-export /requirements.txt /requirements.txt

# Устанавливаем зависимости через pip
RUN pip install -r /requirements.txt

# --- Этап 4: Копирование исходного кода ---
FROM base AS source

# Создаём рабочую директорию
WORKDIR /app

# Копируем исходный код проекта (папка fastapi-application и сопутствующие файлы)
COPY fastapi-application /app/fastapi-application
COPY pyproject.toml /app
COPY README.md /app
COPY .env /app

# Если в проекте есть иные файлы (например, alembic.ini, миграции и т.п.), добавьте их при необходимости:
# COPY alembic.ini /app
# COPY migrations /app/migrations

# --- Этап 5: Финальный образ ---
FROM base AS final

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем установленные пакеты из этапа requirements
COPY --from=requirements /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages

COPY --from=requirements /usr/local/bin /usr/local/bin

# Копируем исходный код из этапа source
COPY --from=source /app /app

# Задаём переменные окружения для приложения (при необходимости)
ENV PORT=8000 HOST=0.0.0.0

ENV PYTHONPATH=/app/fastapi-application
# Команда запуска для основного приложения – запуск uvicorn, который ищет объект app в fastapi-application/main.py
CMD ["uvicorn", "fastapi-application.main:main_app", "--host", "0.0.0.0", "--port", "50000"]
#!/bin/bash

# Загрузка переменных из database_settings.env файла
if [ -f database_settings.env ]; then
    export $(cat database_settings.env | xargs)
else
    echo "database_settings.env file not found!"
    exit 1
fi

# Запуск Docker-контейнера с использованием переменных из database_settings.env файла
docker run --name health_guard_db \
    -e POSTGRES_USER="$POSTGRES_USER" \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$POSTGRES_DB" \
    -p "${POSTGRES_PORT:-5432}":5432 \
    -d postgres

# параметры для запуска контейнера из файла database_settings.env
# POSTGRES_USER: str
# POSTGRES_PASSWORD: str
# POSTGRES_SERVER: str = Field(default="localhost")
# POSTGRES_PORT: int = Field(default=5432)
# POSTGRES_DB: str
# Используем официальный базовый образ Python
FROM python:3.8-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в рабочую директорию
COPY . /app

# Устанавливаем зависимости Python
RUN pip install -r requirements.txt

# Запускаем главный скрипт TTS.py
CMD ["python", "run_script.py"]
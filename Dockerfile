# Базовый образ с Python
FROM python:3.11-slim

# Логи сразу в stdout (без буферизации)
ENV PYTHONUNBUFFERED=1

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем файл зависимостей
COPY app/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем исходный код
COPY app/ .

# При запуске контейнера выполняем наш скрипт
CMD ["python", "main.py"]

# 1. Используем образ Python (лучше подойдет для Django)
FROM python:3.12-slim

# 2. Указываем автора контейнера
LABEL authors="jabko"

# 3. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 4. Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# 5. Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь код проекта в контейнер
COPY . /app/

# 7. Выполняем миграции базы данных
RUN python manage.py migrate

# 8. Устанавливаем точку входа — запуск сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

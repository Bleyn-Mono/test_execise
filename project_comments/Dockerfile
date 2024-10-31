# 1. Используем образ Python для запуска Django
FROM python:3.12-slim

# 2. Указываем автора контейнера
LABEL authors="jabko"

# 3. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 4. Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# 5. Устанавливаем зависимости, включая Gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# 6. Копируем весь код проекта в контейнер
COPY . /app/

# 7. Создаем статические файлы
RUN python manage.py collectstatic --noinput

# 8. Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# 9. Устанавливаем точку входа — запускаем Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_name.wsgi:application"]

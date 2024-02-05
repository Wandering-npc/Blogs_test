FROM python:3.11

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
# RUN docker-compose exec web python3 manage.py migrate --noinput
CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000"]
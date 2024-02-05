FROM python:3.11

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "blog.wsgi:application", "--bind", "0.0.0.0:8000"]
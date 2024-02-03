FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

CMD gunicorn blog.wsgi:application --bind 0.0.0.0:8080
# COPY ./requirements.txt ./
# RUN pip install -r requirements.txt
# COPY . .
#CMD [ "python3", "./src/manage.py", "runserver", "0.0.0.0:8000"]

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --upgrade pip && pip install -r requirements.txt
# COPY . .
# RUN python manage.py collectstatic --noinput
# CMD gunicorn simple_solutions.wsgi:application --bind 0.0.0.0:8080
FROM python:3.8.1-alpine

WORKDIR /usr/src/app

# Prevent Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py run -h 0.0.0.0
FROM python:3.9.0
ENV PYTHONUNBUFFERED 1
WORKDIR /var/www/html/
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
WORKDIR ./PayHere
RUN poetry install
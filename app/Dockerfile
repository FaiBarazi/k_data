FROM python:3.9-alpine
LABEL MAINTAINER="Faisal Albarazi f.barazi@gmail.com"

WORKDIR /src
RUN pip install --upgrade pip
COPY ./requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt

RUN pip install gunicorn
COPY . /src/app


CMD [ "gunicorn", "-w", "2", "--bind", "0.0.0.0:5000", "app.main:application"]


FROM python:3.8.3-slim-buster

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD . /code

COPY . /code

RUN pip install -r requirements.txt

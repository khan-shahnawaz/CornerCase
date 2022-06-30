FROM python:3.8.10-alpine

ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc
RUN pip install --upgrade pip setuptools wheel

RUN apk add musl-dev

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt --default-timeout=100
RUN apk add --no-cache g++


RUN mkdir /CornerCase
COPY . /CornerCase
WORKDIR /CornerCase

FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt

COPY magazin /magazin
WORKDIR /magazin
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password magazin-user
USER magazin-user
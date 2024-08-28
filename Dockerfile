FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY magazin /magazin
WORKDIR /magazin
EXPOSE 8000

# Устанавливаем необходимые зависимости
RUN apk add --no-cache postgresql-client build-base postgresql-dev

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r /temp/requirements.txt

# Добавляем пользователя
RUN adduser --disabled-password magazin-user
USER magazin-user

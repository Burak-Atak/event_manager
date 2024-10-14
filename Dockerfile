FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN apk add gcc musl-dev linux-headers

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

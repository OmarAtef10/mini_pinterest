FROM python:3

WORKDIR /app

ADD . /app

ENV DB_PPASSWORD=1010abab

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app


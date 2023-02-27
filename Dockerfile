FROM python:3.11

COPY requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

WORKDIR /src/api

COPY ./api /src/api

EXPOSE 8000


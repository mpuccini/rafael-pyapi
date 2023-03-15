FROM python:3.11

COPY requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

WORKDIR /src/api

COPY ./api /src/api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

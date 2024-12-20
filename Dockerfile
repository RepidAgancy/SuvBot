FROM python:3.12.8-alpine3.20

WORKDIR /bot

COPY requirements.txt . 

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]

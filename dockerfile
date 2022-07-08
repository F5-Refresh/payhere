FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/payhere

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
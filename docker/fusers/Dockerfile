FROM python:3.9-slim

WORKDIR /opt/app/

COPY fusers-crud/. .
COPY requirements.txt .
RUN pip install gunicorn
RUN pip install -r requirements.txt

EXPOSE 5000

CMD exec gunicorn --bind :5000 run:app --log-level=debug
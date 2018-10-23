FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential python-mysqldb libmysqlclient-dev
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD gunicorn app:app --bind 0.0.0.0:$PORT --reload
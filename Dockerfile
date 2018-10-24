FROM python:latest

RUN mkdir server

ADD . /server

RUN cd server && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

CMD cd server && \
    python app.py 

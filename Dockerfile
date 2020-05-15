FROM python:3.7.6-alpine
WORKDIR /project
ADD . /project
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
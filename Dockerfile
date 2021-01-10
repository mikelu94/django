FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uwsgi", "etc/uwsgi.ini"]

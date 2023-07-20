From python:3.10.6

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim
# 필요한지?
# RUN apt-get -y install python3-dev default-libmysqlclient-dev build-essential
# RUN apt-get -y install mysqlclient

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
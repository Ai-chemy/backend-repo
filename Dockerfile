# base image는 python:3.9로 시작한다.
FROM python:3.9-slim

# python library 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# nginx 설치
RUN apt update \
  && apt install -y nginx

# 기본 service 제거
RUN rm -rf /etc/nginx/sites-enabled/default

# gunicorn과 연결할 설정 복사
COPY nginx.conf /etc/nginx/conf.d

# .venv는 .dockerignore로 인해 복사가 안된다.
WORKDIR /code
COPY . .

# backend port 설정
EXPOSE 8000

# container가 종료될 때 정상종료를 유도한다.
STOPSIGNAL SIGTERM

# django migrate 진행, nginx 시작, gunicorn service 시작. gunicorn이 daemon off로 동작
CMD python manage_docker.py migrate \
  && service nginx start \
  && gunicorn --config gunicorn_config.py aichemy.wsgi:application
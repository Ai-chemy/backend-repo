FROM python:3.10.6

WORKDIR /code

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# nginx 설치
RUN apt update \
  && apt install -y nginx

# 기본 service 제거
RUN rm -rf /etc/nginx/sites-enabled/default

# gunicorn과 연결할 설정 복사
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 8000

# container가 종료될 때 정상종료를 유도한다.
STOPSIGNAL SIGTERM

# django migrate 진행, nginx 시작, gunicorn service 시작. gunicorn이 daemon off로 동작
CMD python manage.py migrate \
  && service nginx start \
  && gunicorn --config gunicorn_config.py aichemy.wsgi:application
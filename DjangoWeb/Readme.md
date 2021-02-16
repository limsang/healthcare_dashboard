## 강석우가 추가로 한일 
 1. ./config/nginx/nginx.conf 넣기
 2. docker-compose.yml
    - volume 추가하기 django_api ( 장고는 Gunicorn 여기에 담는다. )
    - services / web command 변경 : gunicorn -c /django/gunicorn.py rest_server.wsgi:application
 3. gunicorn_cfg.py 내용 변경 및 recsys/gunicorn_cfg.py로 위치 변경
 4. mysite/settings.py
    - ALLOWED_HOSTS에 'web' 추가
## 도커 시작 시
~~~sh
docker-compose up --build
~~~
## 도커 종료 시
~~~sh
docker-compose down --volume
~~~

## 접속시 
http://localhost/admin/
http://localhost/polls/
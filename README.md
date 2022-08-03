# healthcare_dashboard
> 헬스케어 대시보드, 건강과 관련된 내용을 수집하여 대시보드로 제공한다.

> 예측모델을 통해 ~를 제공한다.
 
> 본인의 운동이력을 업로드한다.

# 1. how to run

##### 애플워치, 애플 기본 건강앱에서 기록중인 데이터를 ELK에 저장한다.

[APPLE HEALTH APP ELK 연동 git](https://github.com/markwk/qs_ledger/tree/master/apple_health)

## step.1 xml데이터 csv로 저장
매뉴얼하게 다운로드받은 mxl 데이터를 csv 형식으로 저장
health_data_parser.py 실행
- data 하위 디렉토리에 csv 파일 형식으로 모든 자료가 저장됨

## step.2 gpx데이터 csv로 저장

--- 

### 도커 빌드 및 실행
~~~sh
docker-compose up --build
~~~
## 도커 종료
~~~sh
docker-compose down --volume
~~~

### 접속


~~~sh
python manage.py runserver
~~~
http://127.0.0.1:8000/apmall/item2vec/sample/test

--- 


# 로컬 PC 외부로 공유
## localtunnel 


- 로컬서버를 외부로 등록시켜주는 node.js기반의 오픈소스
- 오픈소스임으로.. 가끔 서버 떨어질 때가있음

$sudo apt install npm

$sudo npm install -g localtunnel

$ lt --port [사용포트번호] --subdomain eames --print-requests

출처: https://kibua20.tistory.com/151 [모바일 SW 개발자가 운영하는 블로그:티스토리]

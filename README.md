# healthcare_dashboard
헬스케어 대시보드


# Apple건강앱 Data ELK 연동
https://github.com/markwk/qs_ledger/tree/master/apple_health

## step.1 xml데이터 csv로 저장
* 매뉴얼하게 다운로드받은 mxl 데이터를 csv 형식으로 저장
health_data_parser.py 실행


## step.2 csv를 elasticsearch index로 생성
* apple_health_data2elastic.py를 실행한다.
mapping은 2가지로, 운동에 대한 인덱스와 기존 정보(걸음, 심박수 등)에 대한 mapping
json 파일로 관리중...


# Django Web App
-> elk CRUD용 API와 머신러닝 API를 생성한다. 
### 도커 빌드 및 실행
~~~sh
docker-compose up --build
~~~
## 도커 종료
~~~sh
docker-compose down --volume
~~~

### 접속
http://localhost/admin/
http://localhost/polls/


~~~sh
python manage.py runserver
~~~
http://127.0.0.1:8000/apmall/item2vec/sample/test


# React frontend
-> API호출용 & 엘라스틱서치 활용을 위한 프론트를 개발한다.



# elk stack
-> docker로 elk stack을 배포한다. 




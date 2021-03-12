# healthcare_dashboard
헬스케어 대시보드, 건강과 관련된 내용을 수집하여 대시보드로 제공한다.

# 1. Apple건강앱 Data ELK 연동

애플워치, 애플 기본 건강앱에서 기록중인 데이터를 ELK에 저장한다.
다음 git에서 소스를 제공 
https://github.com/markwk/qs_ledger/tree/master/apple_health

## step.1 xml데이터 csv로 저장
매뉴얼하게 다운로드받은 mxl 데이터를 csv 형식으로 저장
- health_data_parser.py 실행
- data 하위 디렉토리에 csv 파일 형식으로 모든 자료가 저장됨

## step.2 csv를 elasticsearch index로 생성
* apple_health_data2elastic.py를 실행.
- mapping은 2가지로, 운동에 대한 인덱스와 기존 정보(걸음, 심박수 등)에 대한 mapping
json 파일로 관리중...
- 2021-03-01 기준으로 운동과관련된 mapping이 추가됨.


## step.3 (optional) ndjson파일을 통해 키바나 대시보드를 작성하기 
1. Step 7: Select the button for "Create index pattern" and then type in the name of one of your indexes like steps and hit "Next Step."
2. Step 8: Then use the time field option and select date and hit "Create index pattern."
3. Repeat 6-8 to create additional index patterns for hr and resting_hr.
4. Step 9: Navigate to the menu item "Saved Objects" under Kibana.
5. Step 10: Select option for Import and either drag and drop or select the file apple_health_elastic_dashboard.ndjson which will create a few sample charts and an Apple Health Dashboard which you can view in Kibana.

### 이게뭐냐....??
* 미리 작성한 대시보드가 있다면, 이걸 export해서 나중에 동일한 포맷의 대시보드를 생성할수있게 해주는 작업
1. 키바나의 Saved Object로 이동 
2. 저장한 대시보드를 선택
3. Export를 클릭하면 ndjson 파일을 다운받을 수 있다.
4. 앞의 가이드대로 인덱스패턴을 생성한 후 Import하면 대시보드를 볼 수 있음.



https://support.logz.io/hc/en-us/articles/210207225-How-can-I-export-import-Dashboards-Searches-and-Visualizations-from-my-own-Kibana-


# 2.  Django Web App
-> elk CRUD용 API와 머신러닝 API를 생성한다. 
-> 웹뷰를 통해 여러 정보를 추가로 적재한다. 
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


# React frontend
-> API호출용 & 엘라스틱서치 활용을 위한 프론트를 개발한다.



# elk stack
-> docker로 elk stack을 배포한다. 




# healthcare_dashboard
> 본인의 운동이력을 업로드한다. AppleWatch

> 헬스케어 대시보드, 건강과 관련된 내용을 수집하여 대시보드로 제공한다.

> 예측모델을 통해 ~를 제공한다.
 


# 1. upload workout logs

### 애플워치, 애플 기본 건강앱에서 기록중인 데이터를 rawdata에 업로드한다.

> [로그 데이터 추출방법](http://www.markwk.com/data-analysis-for-apple-health.html)


## step.1 health_data csv로 저장
매뉴얼하게 다운로드받은 mxl 데이터를 csv 형식으로 저장
health_data_parser.py 실행 
- rawdata 하위 디렉토리에 csv 파일 형식으로 모든 자료가 저장됨

## step.2 gpx_data csv로 저장
route_data_parser.py 실행 

- rawdata/workout-routes 하위 디렉토리에 csv 파일 형식으로 모든 자료가 저장됨

--- 

# 2. Streamlit Demo 실행
> run.sh를 실행.



--- 
# 3. 도커로 실행
## run
~~~sh
docker-compose up --build
~~~
## exit
~~~sh
docker-compose down --volume
~~~

--- 
# tips. 

## 1. 로컬 PC 외부로 공유
### localtunnel 

- 로컬서버를 외부로 등록시켜주는 node.js기반의 오픈소스
- 오픈소스임으로.. 가끔 서버 떨어질 때가있음

$sudo apt install npm

$sudo npm install -g localtunnel

$ lt --port [사용포트번호] --subdomain eames --print-requests
[출처: 모바일 SW 개발자가 운영하는 블로그:티스토리](https://kibua20.tistory.com/151)


## 2.  
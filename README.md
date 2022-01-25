# healthcare_dashboard
> 헬스케어 대시보드를 위한 데이터 전처리를 진행

# STEP.1 애플워치에서 데이터 추출
##### 애플워치, 애플 기본 건강앱에서 기록중인 데이터를 ELK에 저장한다.

[APPLE HEALTH APP ELK 연동 git](https://github.com/markwk/qs_ledger/tree/master/apple_health)

## step.1.1 xml데이터 csv로 저장
매뉴얼하게 다운로드받은 mxl 데이터를 csv 형식으로 저장
health_data_parser.py 실행
- data 하위 디렉토리에 csv 파일 형식으로 모든 자료가 저장됨

## step.1.2 gpx데이터 csv로 저장
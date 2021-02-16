FROM python:3.7
# copy requirements.txt ./

# 컨테이너에 /code 디렉토리를 생성
RUN mkdir /code
# /code 디렉토리로 워킹 디렉토리 변경
WORKDIR /code

# 파이썬 로그가 한 발 늦게 출력된다는 느낌을 받을 때 사용
# ENV PYTHONUNBUFFERED=0

# 로컬의 requirements.txt 파일을 /code 디렉토리(절대경로) 하위로 복사
ADD requirements.txt /code/

# 필요 파이썬 패키지를 설치
RUN pip install -r requirements.txt --trusted-host pypi.python.org --trusted-host pypi.org --trusted-host files.pythonhosted.org
# 로컬위치의 모든 파일을 /code/ 디렉토리 하위로 복사
ADD . /code/
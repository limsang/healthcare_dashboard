FROM python:3.7
MAINTAINER lsh9225@naver.com
COPY . /app
WORKDIR /app

#RUN pip install -r requirements.txt
#RUN python -m venv venv
#RUN venv/bin/pip install --upgrade pip
#RUN venv/bin/pip install -r requirements.txt
#CMD . venv/bin/activate && exec python web_demo/main.py
EXPOSE 8501
ENTRYPOINT ["./web_demo/run.sh"]
#ENTRYPOINT ["python", "web_demo/main.py"]
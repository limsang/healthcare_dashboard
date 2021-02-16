FROM python:3.7
# copy requirements.txt ./
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt


EXPOSE 5000 8080 8081
CMD ["python", "app.py"]

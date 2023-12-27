FROM python:3.8-slim
LABEL maintainer="dmitriyburenok@gmail.com"
RUN apt update -y
RUN apt install -y libgl1-mesa-glx libglib2.0-0 gcc curl
COPY . /yolov8-api
WORKDIR /yolov8-api
RUN pip install ultralytics
RUN pip install -r requirements.txt
RUN curl -LO https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
CMD gunicorn --bind 0.0.0.0:8080 api:app -w 1 --threads 4

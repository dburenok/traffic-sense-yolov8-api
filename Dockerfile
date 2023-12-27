FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1
RUN apt update -y
RUN apt install -y libgl1-mesa-glx libglib2.0-0 gcc curl
COPY . /yolov8-api
WORKDIR /yolov8-api
RUN pip install -r requirements.txt
CMD gunicorn --bind 0.0.0.0:8080 api:app --workers 1 --threads 4 --timeout 120

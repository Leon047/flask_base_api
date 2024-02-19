FROM python:3.9
WORKDIR /back
COPY . /back
RUN apt-get update -y &&\
	pip install --upgrade pip &&\
	pip install --no-cache -r requirements.txt

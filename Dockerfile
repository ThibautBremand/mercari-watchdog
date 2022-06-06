FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y install git

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

RUN git submodule update --init --recursive

CMD [ "python3", "-u", "./main.py"]
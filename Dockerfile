
FROM python:3.11-slim

RUN apt-get update
RUN apt install unzip

COPY chrome_114_amd64.deb ./
RUN apt install ./chrome_114_amd64.deb -y

RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver

WORKDIR /app
COPY main.py MultiEmailTool.py requirements.txt ./

RUN pip install -r /app/requirements.txt

RUN echo "starting judging tool"

ENTRYPOINT [ "python", "main.py"]
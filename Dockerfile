FROM python:3.12.1-bullseye

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

CMD python3 bot.py
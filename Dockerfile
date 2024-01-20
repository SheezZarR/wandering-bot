FROM python:3.12-slim

RUN apt update && \
	apt install --no-install-recommends -y locales-all wait-for-it git socat

RUN 
RUN pip install --no-cache-dir --upgrade pip

ADD requirements.txt /srv

RUN pip install --no-cache-dir -r /srv/requirements.txt

WORKDIR /app

COPY src /app
COPY --chmod=766 bot-run.sh /app/bot-run.sh

CMD [] 

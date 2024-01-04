FROM python:3.13-rc-slim

RUN apt update && \
	apt install --no-install-recommends -y locales-all wait-for-it

RUN pip install --no-cache-dir --upgrade pip

ADD requirements.txt /srv

RUN pip install --no-cache-dir -r /srv/requirements.txt


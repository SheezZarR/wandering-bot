FROM python:3.12-slim

RUN apt update && \
	apt install --no-install-recommends -y locales-all wait-for-it git

RUN pip install --no-cache-dir --upgrade pip

ADD requirements.txt /srv

RUN pip install --no-cache-dir -r /srv/requirements.txt

WORKDIR /app

CMD ["python3", "/app/main.py"]


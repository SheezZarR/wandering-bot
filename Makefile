deps:
	pip install pip-tools
	pip-compile requirements.in
	pip-compile dev-requirements.in
	pip-sync requirements.txt dev-requirements.txt
	
lint:
	black src
	isort src
	flake8 src

compdock:
	docker-compose build 
	docker-compose up

# To start a single tg-bot instance...
dock:
	docker build -t tg-bot .
	docker rm tg-bot
	docker run -v /home/SheezZarR/Documents/dev/python/wandering-bot/.env:/app/.env:ro --name tg-bot tg-bot


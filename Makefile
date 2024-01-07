deps:
	pip-compile requirements.in
	pip-compile dev-requirements.in
	pip-sync requirements.txt dev-requirements.txt
	
lint:
	black src
	flake8 src
dock:
	docker build -t tg-bot .
	docker rm tg-bot
	docker run -v /home/SheezZarR/Documents/dev/python/wandering-bot/.env:/app/.env:ro --name tg-bot tg-bot

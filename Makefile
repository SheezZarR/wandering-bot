deps:
	pip-compile requirements.in
	pip-compile dev-requirements.in
	pip-sync requirements.txt dev-requirements.txt
lint:
	black src
	flake8 src


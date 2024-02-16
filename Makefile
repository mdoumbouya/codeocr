authenticate-gcloud:
	export GOOGLE_APPLICATION_CREDENTIALS=keys/gcloud-sacct-cred.json


start-web-app:
	gunicorn -w 4 --threads 2 'main:app' -b 0.0.0.0:8000 --reload --preload --timeout 60

start-dev-server:
	flask --app main run

TODO:



# installing dependencies
.PHONY: install
install:
	pip install -r requirements.txt
	pip install -e .


# Git push simplification
.PHONY: gitpush

gitpush:
	git fetch
	git pull
	git add .
	git commit -m "$(m)"
	git push

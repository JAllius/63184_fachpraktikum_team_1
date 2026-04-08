.PHONY: all clean clean_venv venv build docker deploy_local test

all: venv test deploy_local

clean:
	-rm -rf ./build
	-rm -rf ./src/*.egg-info
	-rm -rf ./.pytest_cache
	-find . \( -name "__pycache__" -o -name "*.pyc" -o -name "*.pyo" \) -exec rm -rf {} +
	-find ./src -empty -type d -delete

clean_venv: clean
	rm -rf ./venv

venv: 
	python3.13 -m venv ./venv/
	./venv/bin/python3 -m pip install --upgrade pip

build: clean 
	./venv/bin/python3 -m pip install -e '.[dev]'

docker: build
	docker compose down -v
	docker build -t 63184_fachpraktikum_team_1-api -f DockerfileApi --no-cache .
	docker build -t 63184_fachpraktikum_team_1-worker -f DockerfileWorker --no-cache . 
	docker build -t 63184_fachpraktikum_team_1-frontend -f DockerfileFrontend  --no-cache .
	docker compose up -d  --remove-orphans --force-recreate

test:
	./venv/bin/python3 -m pip install -e '.[test]'
	./venv/bin/python3 -m pytest

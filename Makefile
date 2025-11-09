clean:
	rm -rf ./build
	rm -rf ./src/*.egg-info
	rm -rf ./.pytest_cache
	rm -rf ./src/**/__pycache__
	rm -rf ./src/**/**/__pycache__
	find ./src -empty -type d -delete

clean_venv: clean
	rm -rf ./venv

venv: 
	python3 -m venv ./venv/

build_app: clean
	./venv/bin/python3 -m pip install .

build_docker: build_app
	docker build -t jallius/fachpraktikum-fastapi .

deploy_local: build_docker
	docker compose up

test: build_app
	./venv/bin/python3 -m pip install -e '.[test]'
	./venv/bin/python3 -m pytest

all: venv test deploy_local
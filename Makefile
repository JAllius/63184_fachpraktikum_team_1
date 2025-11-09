clean:
	rm -rf ./build
	rm -rf ./src/*.egg-info
	rm -rf ./.pytest_cache
	rm -rf ./src/**/__pycache__

clean_venv: clean
	rm -rf ./venv

venv: 
	python3.13 -m venv ./venv/

build: clean
	./venv/bin/python3 -m pip install .

docker: build
	docker build -t jallius/fachpraktikum-fastapi .

deploy_local: docker
	docker compose up

test:
	./venv/bin/python3 -m pip install -e '.[test]'
	./venv/bin/python3 -m pytest

all: venv test deploy_local
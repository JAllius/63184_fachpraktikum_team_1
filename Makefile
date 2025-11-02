clean:
	rm -rf ./build
	rm -rf ./src/*.egg-info

clean_venv: clean
	rm -rf ./venv

venv: clean_venv
	python3 -m venv ./venv/

build_app: clean
	./venv/bin/python3 -m pip install .

build_docker: build_app
	docker build -t jallius/fachpraktikum-fastapi .

deploy_local: build_docker
	docker compose up

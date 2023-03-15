pip/install:
	pip-compile requirements.in
	pip install -r requirements.txt

py/lint:
	pylint ./src

py/test:
	python -m pytest

GIT_HEAD := $(shell git rev-parse HEAD)
docker/build:
	@echo MY_VAR IS $(GIT_HEAD)
	docker build -t lukaskrabbe2/kn:$(GIT_HEAD) .

docker/publish: docker/build
	docker push lukaskrabbe2/kn:$(GIT_HEAD)

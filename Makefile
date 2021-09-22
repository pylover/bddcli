PRJ = bddcli

.PHONY: test
test:
	pytest tests


.PHONY: cover
cover:
	pytest --cov=$(PRJ) tests


.PHONY: lint
lint:
	pylama


.PHONY: dist
dist:
	python setup.py sdist


.PHONY: env
env:
	pip install -r requirements-dev.txt
	pip install -e .



PRJ = bddcli


.PHONY:
coverage:
	pytest --cov=$(PRJ) tests

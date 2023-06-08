test/e2e:
	pytest --html=tests/e2e/e2e-report.html --self-contained-html --css=tests/e2e/e2e.css tests/e2e

code/format:
	unimport -r .
	isort .
	black .

docker/start:
	docker-compose up -d
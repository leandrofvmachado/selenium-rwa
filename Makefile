test/e2e:
	poetry run python -m pytest --html=tests/e2e/e2e-report.html --self-contained-html --css=tests/e2e/e2e.css tests/e2e

code/format:
	poetry run unimport -r .
	poetry run isort .
	poetry run black .
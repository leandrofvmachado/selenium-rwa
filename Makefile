test/e2e: 
	pip3 install -r requirements.txt
	pytest --html=e2e-report.html --self-contained-html --css=assets/e2e.css tests

code/format:
	unimport -r .
	isort .
	black .
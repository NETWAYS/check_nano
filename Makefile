.PHONY: lint test coverage

lint:
	python -m pylint check_nano.py
test:
	python -m unittest -v -b test_check_nano.py
coverage:
	python -m coverage run -m unittest test_check_nano.py
	python -m coverage report -m --include check_nano.py

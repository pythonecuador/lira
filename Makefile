test:
	python -m nox -r -s tests

lint:
	python -m nox -r -s lint

format:
	python -m nox -r -s format

docs:
	python -m nox -r -s docs

clean:
	rm -rf dist/
	rm -rf build/

publish: clean
	python -m pip install --upgrade pip setuptools twine
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

.PHONY: test lint format docs clean publish

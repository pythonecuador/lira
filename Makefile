tests:
	python -m nox -r -s tests

coverage:
	python -m nox -r -s coverage

lint:
	python -m nox -r -s lint

format:
	python -m nox -r -s format

docs:
	python -m nox -r -s docs

serve-docs:
	python -m nox -r -s docs -- --live

clean:
	rm -rf dist/
	rm -rf build/

publish: clean
	python -m pip install --upgrade pip setuptools twine
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

.PHONY: tests lint format docs serve-docs clean publish coverage

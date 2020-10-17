test:
	python -m nox -r -s tests

lint:
	python -m nox -r -s lint

format:
	python -m nox -r -s format

clean:
	rm -rf dist/
	rm -rf build/

publish: clean
	python -m pip install --upgrade pip setuptools twine
	python setup.py sdist bdist_wheel
	python -m twine upload  dist/*

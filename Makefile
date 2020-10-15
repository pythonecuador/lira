clean:
	rm -rf dist/
	rm -rf build/

publish: clean
	python setup.py sdist bdist_wheel
	python -m twine upload  dist/*

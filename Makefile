PYTHON?=python3
BASEDIR=$(CURDIR)

help:
	@echo 'Makefile for OstrichLib                                            '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo '   make test     Run test suite with active Python and PEP8        '
	@echo '   make tox      Run test suite using tox with Python 2.7 & 3.5    '
	@echo '   make lint     Check style for project and tests                 '
	@echo '   make docs     Generate Sphinx HTML documentation                '
	@echo '   make dist     Build source & wheel distributions                '
	@echo '   make clean    Clean build & dist output directories             '
	@echo '   make pypi     Clean, build dist, and upload to PyPI (twine)     '
	@echo '                                                                   '

test:
	py.test --pep8 --cov=ostrich

tox:
	TOXENV=py27,py35 tox

lint_code:
	pylint ostrich

lint_tests:
	find tests -name "*.py" | xargs pylint

lint: lint_tests lint_code

docs:
	cd docs && make html

docs_serve: docs
	cd docs && make serve

dist:
	${PYTHON} setup.py sdist bdist_wheel
	@echo "Finished buliding source & wheel distributions"

clean:
	rm -r $(BASEDIR)/build $(BASEDIR)/dist
	@echo "Finished cleaning build & dist output dirs"

pypi: clean dist
	twine upload dist/*
	@echo "Finished uploading version to PyPI"

.PHONY: help test tox lint_code lint_tests lint docs dist clean pypi

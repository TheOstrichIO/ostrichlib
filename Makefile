help:
	@echo 'Makefile for OstrichLib                                            '
	@echo '                                                                   '
	@echo 'Usage:                                                             '
	@echo '   make test     Run test suite with active Python and PEP8        '
	@echo '   make tox      Run test suite using tox with Python 2.7 & 3.5    '
	@echo '                                                                   '

test:
	py.test --pep8 --cov=ostrich

tox:
	TOXENV=py27,py35 tox

.PHONY: help test tox

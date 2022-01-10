.PHONY: all check generate

all: check generate

check:
	flake8 generate.py --ignore=E501
	pylint generate.py --disable=line-too-long,too-many-locals,too-many-branches,too-many-statements,wrong-import-order

generate:
	python generate.py

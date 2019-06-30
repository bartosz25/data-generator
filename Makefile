.PHONY : setup_project
setup_project:
	python setup.py install

.PHONE : clean_build
clean_build:
	python setup.py clean --all

build_image:
	docker build  -t data_generator:latest -f docker/Dockerfile .

run_image:
	winpty docker run -ti data_generator:latest  bash

test_all:
	pytest data_generator/

lint_all:
	flake8 data_generator/

reformat_all:
	autopep8 --in-place -r data_generator
.PHONY : setup_project
setup_project:
	python setup.py install

.PHONY : create_venv
create_venv:
	virtualenv -p python3 .venv_python3/

.PHONY : activate_venv
activate_venv:
	source .venv_python3/bin/activate

.PHONY : quit_venv
quit_venv:
	deactivate

build_image:
	docker build  -t data_generator:latest -f docker/Dockerfile .

run_image:
	winpty docker run -ti data_generator:latest  bash

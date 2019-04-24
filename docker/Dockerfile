FROM python:3

RUN apt-get update -qq && \
  apt-get install -y python3-pip && \
  apt-get clean

RUN pip install --upgrade pip  && \
  pip3 install virtualenv

# TODO: add user management

RUN mkdir /home/app
# A lot of problems with egg ==> try to run it on Ubuntu and only if it works, do the same on Windows
# But not sure it will work because maybe the compilation & the runtime envs will be different and
# it's overall better to execute it in classical manner
#COPY ./course_data_generator/dist/Data_engineer_course_data_generator-0.0.1-py3.6.egg /home/app/app_0.0.1.egg
#COPY ./dist/Data_engineer_course_data_generator-0.0.1-py3.6.egg /home/app/app_0.0.1.egg

COPY ./ /home/app/
COPY ./docker/entrypoint.sh /entrypoint.sh

# Create virtualenv
WORKDIR /home/app/
RUN virtualenv -p python3 .venv_python3/
RUN /bin/bash -c "source .venv_python3/bin/activate"
RUN pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
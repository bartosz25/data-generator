FROM python:3

RUN apt-get update -qq && \
  apt-get install -y python3-pip && \
  apt-get install -y librdkafka-dev && \
  apt-get clean

RUN pip install --upgrade pip  && \
  pip3 install virtualenv


RUN useradd -ms /bin/bash  data_generator
USER data_generator
WORKDIR /home/data_generator


COPY docker/kafka/assets ./assets

RUN virtualenv -p python3 .venv/
RUN /bin/bash -c "source .venv/bin/activate"

RUN pip3 install ./assets/HTTP_logs_web_visits_data_generator-0.0.1-py2.py3-none-any.whl



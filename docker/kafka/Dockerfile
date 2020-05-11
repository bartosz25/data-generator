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


#COPY docker/kafka/assets ./assets

COPY requirements.txt ./
COPY data_generator ./data_generator

RUN virtualenv -p python3 .venv/
RUN /bin/bash -c "source .venv/bin/activate"

RUN pip3 install -r requirements.txt

COPY examples ./examples
RUN ls ./

ENTRYPOINT python3 /home/data_generator/examples/kafka/generate_dataset_to_kafka.py


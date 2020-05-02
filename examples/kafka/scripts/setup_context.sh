#!/bin/bash

# We run here a separate script just to not keep KafkaAdmin connections
# open. It happens when we use a `kafka-topics.sh` for every created
# topic. Normally this shell command will remain an active process
# but it will do nothing so its impact can be neglected.
# This was the easiest method to setup Kafka topics automatically
# after Kafka bootstrap.
echo "Scheduled topics (raw_data, valid_data, invalid_data, sessions) creation"
/start_topics.sh &
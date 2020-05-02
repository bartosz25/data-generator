#!/bin/bash
kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic raw_data --partitions 5 --replication-factor 1
kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic valid_data --partitions 5 --replication-factor 1
kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic invalid_data --partitions 5 --replication-factor 1
kafka-topics.sh --create  --bootstrap-server localhost:9092 --topic sessions --partitions 5 --replication-factor 1



echo ">> TOPICS (raw_data, valid_data, invalid_data, sessions) were correctly created"
exit;
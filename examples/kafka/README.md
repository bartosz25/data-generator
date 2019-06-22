# Apache Kafka sink example

An example of generator writing data to an Apache Kafka topic. 

# How to run?
1. Start Apache Kafka and Apache Zookeeper containers: `docker-compose up`
2. Start generation script: `python generate_dataset_to_kafka.py`
3. Check generated messages by:
    1. `docker ps` to verify the container running Apache Kafka broker (e.g. fea4e445bc3c)
    2. `docker exec -ti fea4e445bc3c  bash` to access the bash of Kafka's container
    3. `kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic raw_data` to see incoming messages.
    Remember to disconnect every time you restart the generation. Otherwise topic recreation won't work.
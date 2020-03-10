import time

from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import Producer, NewTopic


class KafkaWriterConfiguration:
    def __init__(self, configuration):
        self.broker = configuration['broker']
        self.topics = []
        for topic_name, topic_configuration in configuration['topics'].items():
            self.topics.append(KafkaConfigurationTopic(topic_name, topic_configuration['replication'],
                                                       topic_configuration['partitions']))
        self.producer = None
        self.producer_configuration = configuration['producer']['configuration']

    def create_or_recreate_topics(self):
        admin = AdminClient({'bootstrap.servers': self.broker})
        topics_to_delete = list(map(lambda topic_spec: topic_spec.name, self.topics))

        deleted_topics_result = admin.delete_topics(topics_to_delete, operation_timeout=15, request_timeout=45)
        for deleted_topic, future in deleted_topics_result.items():
            try:
                future.result()
            except Exception as e:
                # TODO: transform to WARN
                print('An error occurred on deleting {}: {}'.format(deleted_topic, e))

        # Apparently there is a concurrent issue with topics create or recreate operations
        # https://github.com/confluentinc/confluent-kafka-python/issues/524
        # That's why I will try to create the topic 5 times with a kind of exponential backoff
        topics_to_create = {topic_spec.name: topic_spec.to_new_topic() for topic_spec in self.topics}
        creation_errors = {}
        for retry in range(0, 5):
            if not topics_to_create:
                break
            futures = admin.create_topics(list(topics_to_create.values()), operation_timeout=15, request_timeout=45)
            for topic, f in futures.items():
                try:
                    f.result()
                    print("Topic {} created".format(topic))
                    topics_to_create.pop(topic, None)
                except Exception as e:
                    print("Topic {} was not created {} - retrying".format(topic, e))  # TODO: transform to warning
                    if retry == 4:
                        creation_errors.append((topic, e))
            time.sleep(retry*5)

        assert not creation_errors, "Some topics were not correctly created {}".format(
            list(map(lambda topic_and_error: "{}: {}".format(topic_and_error[0], topic_and_error[1]), creation_errors))
        )

    def send_message(self, topic_name, key, message):
        if not self.producer:
            # check https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md for more information
            producer_config = {'bootstrap.servers': self.broker}
            producer_config.update(self.producer_configuration)
            self.producer = Producer(producer_config)
        """
        Traceback (most recent call last):
        File "/home/bartosz/workspace/data-generator/examples/kafka/generate_dataset_to_kafka.py", line 51, in <module>
            configuration.send_message(output_topic_name, action)
        File "/home/bartosz/workspace/data-generator/data_generator/sink/kafka_writer.py", line 60, in send_message
            self.producer.produce(topic_name, value=bytes(message, encoding='utf-8'))
        BufferError: Local: Queue full
        The below code is the workaround for the above problem, found here:
        `Confluent Kafka-Python issue 104 <https://github.com/confluentinc/confluent-kafka-python/issues/104>`
        """
        try:
            self.producer.produce(topic=topic_name, key=bytes(key, encoding='utf-8'),
                                  value=bytes(message, encoding='utf-8'))
        except BufferError:
            self.producer.flush()
            self.producer.produce(topic=topic_name, key=bytes(key, encoding='utf-8'),
                                  value=bytes(message, encoding='utf-8'))

    def __repr__(self):
        return 'KafkaWriterConfiguration (broker={}) (topics={})'.format(self.broker, self.topics)


class KafkaConfigurationTopic:
    def __init__(self, name, replication, partitions):
        self.name = name
        self.replication = replication
        self.partitions = partitions

    def to_new_topic(self):
        return NewTopic(self.name, num_partitions=self.partitions, replication_factor=self.replication)

    def __repr__(self):
        return 'Kafka topic {} (repl={}, part={})'.format(self.name, self.replication, self.partitions)

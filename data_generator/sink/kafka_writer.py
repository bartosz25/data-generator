import json
import logging

from kafka import KafkaProducer

logger = logging.getLogger(__name__)


class KafkaWriterConfiguration:
    def __init__(self, configuration):
        self.broker = configuration['broker']
        self.topics = []
        for topic_name, topic_configuration in configuration['topics'].items():
            self.topics.append(KafkaConfigurationTopic(topic_name, topic_configuration['replication'],
                                                       topic_configuration['partitions'],
                                                       topic_configuration['recreate']))
        self.producer = None
        self.producer_configuration = configuration['producer']['configuration']

    def create_or_recreate_topics(self, admin=None):
        topics_to_recreate = list(filter(lambda topic_spec: topic_spec.recreate, self.topics))
        if topics_to_recreate:
            raise Exception("Topic recreation is not implemented in this version")

    def send_message(self, topic_name, key, message):
        if not self.producer:
            # check https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md for more information
            producer_config = {'bootstrap_servers': self.broker,
                               'value_serializer': lambda m: json.dumps(m).encode('utf-8')
                               }
            # TODO: imlement me later producer_config.update(self.producer_configuration)
            self.producer = KafkaProducer(**producer_config)
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

        def delivery_callback(error):
            logger.error("Record was not correctly delivered: %s", error)

        try:
            self.producer.send(topic=topic_name, key=key.encode('utf-8'),
                               value=json.loads(message)).add_errback(delivery_callback)
        except BufferError:
            self.producer.flush()
            self.producer.send(topic=topic_name, key=key.encode('utf-8'),
                               value=json.loads(message)).add_errback(delivery_callback)

    def __repr__(self):
        return 'KafkaWriterConfiguration (broker={}) (topics={})'.format(self.broker, self.topics)


class KafkaConfigurationTopic:
    def __init__(self, name, replication, partitions, recreate):
        self.name = name
        self.replication = replication
        self.partitions = partitions
        self.recreate = recreate

    def to_new_topic(self):
        # TODO: put back later return NewTopic
        # (self.name, num_partitions=self.partitions, replication_factor=self.replication)
        pass

    def __repr__(self):
        return 'Kafka topic {} (repl={}, part={}, recreate={})'.format(self.name, self.replication,
                                                                       self.partitions, self.recreate)

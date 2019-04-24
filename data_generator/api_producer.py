from kafka import KafkaProducer


def create_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting to Kafka: {}'.format(ex))
    finally:
        return _producer


def send_to_api(message, producer, topic_name):
    """
    Even though the name is send_to_api, it's purely informational because we will bypass this extra
    layer and insert the message directly to the Apache Kafka topic.
    """
    try:
        producer.send(topic_name, value=bytes(message, encoding='utf-8'))
        # TODO to me: for now I will test that without explicit flush method
    except Exception as ex:
        print('An error occurred during the sending of the message {message}. The error was: {error}'.format(
            message=message, error=ex))


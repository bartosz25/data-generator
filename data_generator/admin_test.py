from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

admin = AdminClient({'bootstrap.servers': '173.18.0.20:9092'})

futures = admin.create_topics([NewTopic('test-1', num_partitions=1, replication_factor=1)], request_timeout=15)

for topic, f in futures.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        print("Failed to create topic {}: {}".format(topic, e))
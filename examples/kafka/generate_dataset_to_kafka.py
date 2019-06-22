from random import uniform, randint
from time import sleep

import datetime
# Hack to be able to execute data-generator script without needing to compile it
# If you have any better idea how to achieve that, please comment
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..', 'data-generator')))

from data_generator.model.dataset import Dataset
from data_generator.sink.kafka_writer import KafkaWriterConfiguration

if __name__ == '__main__':
    dataset = Dataset(duration_min_seconds=10, duration_max_minutes=30,
                      percentage_incomplete_data=2, percentage_inconsistent_data=2,
                      percentage_app_v1=20, percentage_app_v2=20,
                      users_number=10
                      )

    def should_send_message():
        return randint(0, 1)

    output_topic_name = 'raw_data'
    configuration = KafkaWriterConfiguration({
        'broker': '160.0.0.20:9092',
        'topics': {
            output_topic_name: {'partitions': 1, 'replication': 1}
        },
        'producer': {
            'configuration': {
                'queue.buffering.max.ms': 2000  # flush buffer every 2 seconds
            }
        }
    })
    configuration.create_or_recreate_topics()

    while True:
        now = int(datetime.datetime.utcnow().timestamp())
        for index, visit in enumerate(dataset.visits):
            if visit.is_active(now):
                action = visit.generate_new_action(dataset.pages)
                # We don't send the message every time. The visit can be shorter or longer, and this
                # flip of a coin helps to simulate longer visit.
                if should_send_message():
                    # sleep a random time to better simulate the real-world behavior
                    sleep(uniform(0.0, 1.3))
                    configuration.send_message(output_topic_name, action)
            else:
                print('Terminating {}'.format(visit))
                dataset.reinitialize_visit(visit)

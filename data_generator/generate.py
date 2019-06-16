from random import uniform, randint
from time import sleep

from data_generator.api_producer import send_to_api, create_kafka_producer
from data_generator.model.dataset import Dataset


if __name__ == '__main__':
    dataset = Dataset(duration_min_seconds=10, duration_max_minutes=30,
                      percentage_incomplete_data=2, percentage_inconsistent_data=2,
                      percentage_app_v1=20, percentage_app_v2=20,
                      users_number=10
                      )

    def should_send_message():
        return randint(0, 1)

    while True:
        producer = create_kafka_producer()
        topic_name = 'test-topic-data'
        for index, visit in enumerate(dataset.visits):
            if visit.is_active():
                action = visit.generate_new_action(dataset.pages)
                # We don't send the message every time. The visit can be shorter or longer, and this
                # flip of a coin helps to simulate longer visit.
                if should_send_message():
                    # sleep a random time to better simulate the real-world behavior
                    sleep(uniform(0.0, 1.3))
                    send_to_api(action, producer, topic_name)
                    print('sending {}'.format(action))
            else:
                print('Terminating {}'.format(visit))
                dataset.reinitialize_visit(visit)

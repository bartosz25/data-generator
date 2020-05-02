import os
# Hack to be able to execute data-generator script without needing to compile it
# If you have any better idea how to achieve that, please comment
import sys
from random import randint, choice

from data_generator.sink.kinesis_writer import KinesisWriterConfiguration

sys.path.append(os.path.abspath(os.path.join('..', 'data-generator')))

from data_generator.model.unordered_data import UnorderedDataContainer
from data_generator.model.timer import Timer
from data_generator.model.dataset import Dataset

if __name__ == '__main__':
    dataset = Dataset(duration_min_seconds=10, duration_max_seconds=300,
                      percentage_incomplete_data=2, percentage_inconsistent_data=2,
                      percentage_app_v1=20, percentage_app_v2=20,
                      users_number=3000, timer=Timer(latency_seconds=-900)
                      )

    unordered_data_container = UnorderedDataContainer(lambda: choice([0] * 90 + [1] * 10))


    def should_send_unordered_actions():
        flags = [0] * 90 + [1] * 10
        return choice(flags)


    output_stream_name = 'data-generator-test'
    configuration = KinesisWriterConfiguration({
        'topics': {
            output_stream_name: {'shards': 1}
        }
    })
    configuration.create_or_recreate_streams()

    def get_random_duration_in_seconds():
        return randint(1, 10)


    while True:
        for index, visit in enumerate(dataset.visits):
            if visit.output_log_to_the_sink():
                action = visit.generate_new_action(dataset.pages, get_random_duration_in_seconds())
                unordered_data_container.wrap_action(action,
                                                     lambda generated_action: configuration.send_messages(
                                                         output_stream_name, generated_action
                                                     ))
            elif visit.is_to_close:
                dataset.reinitialize_visit(visit)

            if should_send_unordered_actions():
                unordered_data_container.send_buffered_actions(
                    lambda late_action: configuration.send_messages(output_stream_name, late_action))

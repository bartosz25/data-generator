import datetime
import json
import logging
import os
import random

import sys

sys.path.append(os.path.abspath(os.path.join('..', 'data-generator')))
from data_generator.model.dataset import Dataset
from data_generator.model.timer import Timer
from data_generator.sink.local_filesystem_writer import LocalFileSystemConfiguration

logging.basicConfig(filename='/tmp/logs_writer.txt', level=logging.DEBUG, format='%(asctime)s %(message)s')

if __name__ == '__main__':
    timer = Timer(-3*24*60*60)  # starting from 3 days ago
    dataset = Dataset(duration_min_seconds=120, duration_max_seconds=600,
                      percentage_incomplete_data=2, percentage_inconsistent_data=2,
                      percentage_app_v1=20, percentage_app_v2=20,
                      users_number=10000, timer=timer
                      )

    def get_random_duration_in_seconds():
        return random.randint(1, 10)

    def _extract_event_time(json_data):
        json_object = json.loads(json_data)
        # TODO: try to format it with a datetime formatter
        event_time = json_object['event_time']
        return '{day}/{month}/{year}/{hour}'.format(day=event_time[0:4], month=event_time[5:7],
                                                    year=event_time[8:10], hour=event_time[11:13])

    configuration = LocalFileSystemConfiguration(
        partition_getter=_extract_event_time,
        max_in_partition=200000,
        base_dir='/tmp/sessions/input',
        inactivity_delay=datetime.timedelta(minutes=10)
    )

    while True:
        for index, visit in enumerate(dataset.visits):
            action = visit.generate_new_action(dataset.pages, get_random_duration_in_seconds())
            configuration.add_log(action)
            if visit.is_to_close:
                dataset.reinitialize_visit(visit)

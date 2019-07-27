import datetime
import logging
import os
import shutil
import uuid
from collections import defaultdict

logger = logging.getLogger('LocalFileSystemConfiguration')


class LocalFileSystemConfiguration:
    def __init__(self, partition_getter, max_in_partition, base_dir, inactivity_delay):
        self.partition_getter = partition_getter
        self.data_per_partition = defaultdict(lambda: [])
        self.timeout_per_partition = {}
        self.max_in_partition = max_in_partition
        self.inactivity_delay = inactivity_delay

        os.makedirs(base_dir, exist_ok=True)
        # clean the directory if needed
        shutil.rmtree(base_dir)
        self.base_dir = base_dir

    def add_log(self, log_json):
        partition = self.partition_getter(log_json)
        self.data_per_partition[partition].append(log_json)
        # start by checking partitions to output by their timeout
        # we could do it in background task at regular interval but let's keep things simple
        timeout_to_delete = []
        for partition_key, timeout in self.timeout_per_partition.items():
            if timeout < datetime.datetime.now():
                self._write_partition_data(partition_key)
                timeout_to_delete.append(partition_key)

        for key in timeout_to_delete:
            del self.timeout_per_partition[key]

        if len(self.data_per_partition[partition]) >= self.max_in_partition:
            self._write_partition_data(partition)

        self.timeout_per_partition[partition] = datetime.datetime.now() + self.inactivity_delay

    def _write_partition_data(self, partition_key):
        logger.info('Writing logs for {}'.format(partition_key))
        file_name = str(uuid.uuid4())

        partitioned_dir_path = '{}/{}'.format(self.base_dir, partition_key)
        os.makedirs(partitioned_dir_path, exist_ok=True)
        file_path = '{}/{}.json'.format(partitioned_dir_path, file_name)
        output_file = open(file_path, 'w+')
        for json_line in self.data_per_partition[partition_key]:
            output_file.write(json_line)
        output_file.close()
        logger.info('Written logs to {}'.format(file_path))
        self.data_per_partition[partition_key] = []

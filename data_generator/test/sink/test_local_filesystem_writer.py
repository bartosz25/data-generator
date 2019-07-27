import datetime
import glob
from time import sleep

from assertpy import assert_that

from data_generator.sink.local_filesystem_writer import LocalFileSystemConfiguration


def should_add_log_and_not_output_the_file():
    base_dir = '/tmp/test_local_file_system_writer/not_output_the_file'
    configuration = LocalFileSystemConfiguration(
        partition_getter=lambda text: text[0],
        max_in_partition=30,
        base_dir=base_dir,
        inactivity_delay=datetime.timedelta(minutes=10)
    )

    configuration.add_log('test')

    files = [f for f in glob.glob(base_dir + "**/*.json", recursive=True)]

    assert_that(files).is_empty()


def should_add_log_and_write_output_file_after_timeout():
    base_dir = '/tmp/test_local_file_system_writer/output_the_file_timeout'
    configuration = LocalFileSystemConfiguration(
        partition_getter=lambda text: text[0],
        max_in_partition=30,
        base_dir=base_dir,
        inactivity_delay=datetime.timedelta(seconds=2)
    )
    configuration.add_log('test')
    sleep(3)
    configuration.add_log('aest2')
    sleep(3)
    configuration.add_log('xest2')

    files_for_t = [f for f in glob.glob(base_dir + "/t/*.json", recursive=True)]
    files_for_a = [f for f in glob.glob(base_dir + "/a/*.json", recursive=True)]

    assert_that(files_for_t).is_length(1)
    assert_that(files_for_a).is_length(1)


def should_add_2_logs_and_output_file_because_of_the_size_condition():
    base_dir = '/tmp/test_local_file_system_writer/output_the_file_size'
    configuration = LocalFileSystemConfiguration(
        partition_getter=lambda text: text[0],
        max_in_partition=2,
        base_dir=base_dir,
        inactivity_delay=datetime.timedelta(seconds=120)
    )
    configuration.add_log('test')
    configuration.add_log('aest2')
    configuration.add_log('test2')

    files_for_t = [f for f in glob.glob(base_dir + "/t/*.json", recursive=True)]
    files_for_a = [f for f in glob.glob(base_dir + "/a/*.json", recursive=True)]

    assert_that(files_for_t).is_length(1)
    assert_that(files_for_a).is_empty()

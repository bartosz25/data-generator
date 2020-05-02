import pathlib
from collections import Counter

import yaml
from assertpy import assert_that

from data_generator.model.dataset import Dataset
from data_generator.model.entities import DataAnomaly
from data_generator.model.timer import Timer


def should_generate_pages_map():
    page_map = Dataset.create_page_map()

    expected_map = {'category 17': [
        'category 1', 'category 2', 'category 3', 'category 4', 'category 5', 'category 6',
        'category 7', 'category 8', 'category 9', 'category 10', 'category 11', 'category 12',
        'category 13', 'category 14', 'category 15', 'category 16', 'category 17', 'category 18',
        'category 19', 'category 20', 'category 21', 'category 22', 'category 23', 'category 24',
        'category 25', 'index', 'about', 'my-account', 'article category 17-1', 'article category 17-2',
        'article category 17-3', 'article category 17-4', 'article category 17-5',
        'article category 17-6', 'article category 17-7', 'article category 17-8',
        'article category 17-9', 'article category 17-10', 'article category 17-11',
        'article category 17-12', 'article category 17-13', 'article category 17-14',
        'article category 17-15', 'article category 17-16', 'article category 17-17', 'article category 17-18',
        'article category 17-19', 'article category 17-20', 'article category 17-21', 'article category 17-22',
        'article category 17-23', 'article category 17-24', 'article category 17-25'
    ], 'article category 25-17': [
        'category 1', 'category 2', 'category 3', 'category 4', 'category 5', 'category 6', 'category 7',
        'category 8', 'category 9', 'category 10', 'category 11', 'category 12', 'category 13', 'category 14',
        'category 15', 'category 16', 'category 17', 'category 18', 'category 19', 'category 20', 'category 21',
        'category 22', 'category 23', 'category 24', 'category 25', 'index', 'about', 'my-account'
    ], 'about': [
        'index', 'about', 'my-account', 'category 1', 'category 2', 'category 3', 'category 4', 'category 5',
        'category 6', 'category 7', 'category 8', 'category 9', 'category 10', 'category 11', 'category 12',
        'category 13', 'category 14', 'category 15', 'category 16', 'category 17', 'category 18', 'category 19',
        'category 20', 'category 21', 'category 22', 'category 23', 'category 24', 'category 25'
    ]}

    for page_name, linked_pages in expected_map.items():
        assert_that(page_map[page_name]).contains_sequence(*linked_pages)


def should_create_correct_apps_distribution():
    versions_distribution = Dataset.create_versions_distribution(50, 10, 10, 80)

    versions_count = {'v1': 0, 'v2': 0, 'v3': 0}
    for version in versions_distribution:
        versions_count[version] += 1

    assert_that(versions_count['v1']).is_equal_to(5)
    assert_that(versions_count['v2']).is_equal_to(5)
    assert_that(versions_count['v3']).is_equal_to(40)


def should_create_correct_data_anomalies_distribution():
    data_anomalies_distribution = Dataset.create_data_anomalies_distribution(60, 10, 12)

    anomalies_count = {DataAnomaly.MISSING: 0, DataAnomaly.INCOMPLETE_DATA: 0, DataAnomaly.INCONSISTENT_DATA: 0}
    for anomaly in data_anomalies_distribution:
        anomalies_count[anomaly] += 1

    # The sum is not equal to 60 but it's a rounding issue that doesn't worth to be solved right now because of
    # too small impact on the system
    assert_that(anomalies_count[DataAnomaly.MISSING]).is_equal_to(47)
    assert_that(anomalies_count[DataAnomaly.INCOMPLETE_DATA]).is_equal_to(6)
    assert_that(anomalies_count[DataAnomaly.INCONSISTENT_DATA]).is_equal_to(8)


def should_create_keep_private_flags_distribution():
    keep_private_flags_distribution = Dataset.create_keep_private_flags_distribution(50, 25)

    keep_private_count = {True: 0, False: 0}
    for flag in keep_private_flags_distribution:
        keep_private_count[flag] += 1

    assert_that(keep_private_count[True]).is_equal_to(13)
    assert_that(keep_private_count[False]).is_equal_to(37)


def should_create_a_correct_number_of_visits():
    dataset = Dataset(10, 30, percentage_incomplete_data=1, percentage_inconsistent_data=1, percentage_app_v1=10,
                      percentage_app_v2=15, users_number=100, timer=Timer(-900), no_data_consent_percentage=2)

    assert_that(dataset.visits).is_length(100)


def should_reinitialize_a_visit_with_random_duration():
    dataset = Dataset(10, 30, percentage_incomplete_data=1, percentage_inconsistent_data=1, percentage_app_v1=10,
                      percentage_app_v2=15, users_number=100, timer=Timer(-900), no_data_consent_percentage=2)
    first_visit = dataset.visits[0]

    initial_app_version = first_visit.app_version
    initial_anomaly = first_visit.data_anomaly
    initial_attributes = {**first_visit.__dict__}

    dataset.reinitialize_visit(first_visit)

    assert_that(first_visit.app_version).is_equal_to(initial_app_version)
    assert_that(first_visit.data_anomaly).is_equal_to(initial_anomaly)
    # assert only on the fields that are certainly different every time
    assert_that(first_visit.visit_id).is_not_equal_to(initial_attributes['visit_id'])
    assert_that(first_visit.user_id).is_not_equal_to(initial_attributes['user_id'])
    assert_that(first_visit.duration_seconds).is_not_equal_to(initial_attributes['duration_seconds'])


def should_create_dataset_from_yaml_configuration():
    path = pathlib.Path(__file__).parent.absolute()
    with open('{}/dataset_configuration.yaml'.format(path)) as file:
        configuration = yaml.load(file, Loader=yaml.FullLoader)

    dataset = Dataset.from_yaml(configuration)

    counted_versions = Counter(dataset.versions_to_distribute)
    assert_that(counted_versions['v1']).is_equal_to(200)
    assert_that(counted_versions['v2']).is_equal_to(200)
    assert_that(counted_versions['v3']).is_equal_to(600)
    assert_that(dataset.timer.latency_seconds).is_equal_to(-900)
    data_quality_issues = Counter(dataset.data_anomalies_distribution)
    assert_that(data_quality_issues[DataAnomaly.MISSING]).is_equal_to(960)
    assert_that(data_quality_issues[DataAnomaly.INCOMPLETE_DATA]).is_equal_to(20)
    assert_that(data_quality_issues[DataAnomaly.INCONSISTENT_DATA]).is_equal_to(20)
    assert_that(dataset._Dataset__duration_min).is_equal_to(10)
    assert_that(dataset._Dataset__duration_max).is_equal_to(300)

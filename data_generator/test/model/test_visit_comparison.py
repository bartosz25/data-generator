import json

from assertpy import assert_that

from data_generator.model.entities import DataAnomaly
from data_generator.model.timer import Timer
from data_generator.model.visit import Visit
from data_generator.test import generators_for_tests, assertions_for_test


def should_generate_2_different_events_for_the_same_visit_without_anomaly():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.MISSING,
                  timer=Timer(-900), keep_private=False)

    action_1 = json.loads(visit.generate_new_action(test_pages, 30))
    action_2 = json.loads(visit.generate_new_action(test_pages, 10))

    assertions_for_test.assert_visits_consistency(action_1, action_2)


def should_generate_2_different_events_for_the_same_visit_with_incomplete_data_anomaly():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.INCOMPLETE_DATA,
                  timer=Timer(-900), keep_private=False)

    action_1 = json.loads(visit.generate_new_action(test_pages, 20))
    action_2 = json.loads(visit.generate_new_action(test_pages, 10))

    assertions_for_test.assert_visits_consistency(action_1, action_2)


def should_generate_2_different_events_for_the_same_visit_with_inconsistent_data_anomaly():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.INCONSISTENT_DATA,
                  timer=Timer(-900), keep_private=False)

    action_1 = json.loads(visit.generate_new_action(test_pages, 10))
    action_2 = json.loads(visit.generate_new_action(test_pages, 20))

    assertions_for_test.assert_visits_consistency(action_1, action_2)


def should_generate_the_next_action_not_closing_the_visit():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.INCONSISTENT_DATA,
                  timer=Timer(-900), keep_private=False)

    json.loads(visit.generate_new_action(test_pages, 110))

    assert_that(visit.is_to_close).is_false()


def should_generate_the_next_action_closing_the_visit():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.INCONSISTENT_DATA,
                  timer=Timer(-900), keep_private=False)

    json.loads(visit.generate_new_action(test_pages, 130))

    assert_that(visit.is_to_close).is_true()


def should_generate_invalid_log():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.MISSING,
                  timer=Timer(-900), keep_private=False)

    invalid_visit_log = json.loads(visit.generate_new_action(test_pages, 30, False))

    assert_that(invalid_visit_log['visit_id']).is_none()

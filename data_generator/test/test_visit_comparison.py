import json

from data_generator.model.entities import DataAnomaly, generate_event
from data_generator.test import generators_for_tests, assertions_for_test
from data_generator.visit import Visit


def should_generate_2_different_events_for_the_same_visit_without_anomaly():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.MISSING)

    action_1 = json.loads(visit.generate_new_action(test_pages))
    action_2 = json.loads(visit.generate_new_action(test_pages))

    assertions_for_test.assert_visits_consistency(action_1, action_2)


def should_generate_2_different_events_for_the_same_visit_with_incomplete_data_anomaly():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.INCOMPLETE_DATA)

    action_1 = json.loads(visit.generate_new_action(test_pages))
    action_2 = json.loads(visit.generate_new_action(test_pages))

    assertions_for_test.assert_visits_consistency(action_1, action_2)


def should_generate_2_different_events_for_the_same_visit_with_inconsistent_data_anomaly():
    test_pages = generators_for_tests.generate_pages_map()
    visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.INCONSISTENT_DATA)

    action_1 = json.loads(visit.generate_new_action(test_pages))
    action_2 = json.loads(visit.generate_new_action(test_pages))

    assertions_for_test.assert_visits_consistency(action_1, action_2)

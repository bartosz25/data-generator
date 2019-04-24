from model.entities import DataAnomaly, generate_event
from visit import Visit


def should_generate_2_different_events_for_the_same_visit_without_anomaly():
    visit = Visit(visit_duration=120, app_version='v1', data_anomaly=DataAnomaly.MISSING)

    event_1 = generate_event(visit)
    event_2 = generate_event(visit)

    print('{}'.format(event_1))
    print('{}'.format(event_2))


def should_generate_2_different_events_for_the_same_visit_with_incomplete_data_anomaly():
    visit = Visit(visit_duration=120, app_version='v1', data_anomaly=DataAnomaly.INCOMPLETE_DATA)

    event_1 = generate_event(visit)
    event_2 = generate_event(visit)

    print('{}'.format(event_1))
    print('{}'.format(event_2))


def should_generate_2_different_events_for_the_same_visit_with_inconsistent_data_anomaly():
    visit = Visit(visit_duration=120, app_version='v1', data_anomaly=DataAnomaly.INCONSISTENT_DATA)

    event_1 = generate_event(visit)
    event_2 = generate_event(visit)

    print('INCNSIT {}'.format(event_1))
    print('INSCT {}'.format(event_2))

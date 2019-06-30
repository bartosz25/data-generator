import datetime

from assertpy import assert_that

from data_generator.model.entities import DataAnomaly
from data_generator.model.visit import Visit


def should_create_visit_with_incomplete_data():
    visit = Visit(30, 'v1', DataAnomaly.INCOMPLETE_DATA)

    incomplete_fields_candidates = [visit.device, visit.network, visit.browser, visit.source]

    incomplete_fields = list(filter(lambda value: not value, incomplete_fields_candidates))

    assert_that(incomplete_fields).is_length(2)


def should_create_visit_with_inconsistent_data():
    visit = Visit(30, 'v1', DataAnomaly.INCONSISTENT_DATA)
    def is_dict(field): return type(field) is dict
    def starts_with_www(field): return field.startswith('www.')

    inconsistenf_fields = list(filter(lambda result: result, [is_dict(visit.device), is_dict(visit.network),
                                                              is_dict(visit.browser), starts_with_www(visit.source)]))
    assert_that(inconsistenf_fields).is_length(2)


def should_make_a_visit_inactive_after_visit_expiration():
    visit = Visit(2, 'v1', DataAnomaly.INCONSISTENT_DATA)
    now = int(datetime.datetime.utcnow().timestamp())

    assert_that(visit.is_active(now)).is_true()
    # for 2 seconds, the visit should still be considered as active
    timestamp_2_secs_later = now + 2
    assert_that(visit.is_active(timestamp_2_secs_later)).is_true()
    # wait now 3 seconds and check whether the visit becomes inactive
    timestamp_3_secs_later = now + 3
    assert_that(visit.is_active(timestamp_3_secs_later)).is_false()

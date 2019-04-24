from assertpy import assert_that

from model.entities import DataAnomaly
from visit import Visit


def should_create_visit_with_incomplete_data():
    visit = Visit(30, 'v1', DataAnomaly.INCOMPLETE_DATA)

    incomplete_fields_candidates = [visit.device, visit.network, visit.browser, visit.source]

    incomplete_fields = list(filter(lambda value: not value, incomplete_fields_candidates))
    assert_that(incomplete_fields).is_length(2)


def should_create_visit_with_inconsistent_data():
    visit = Visit(30, 'v1', DataAnomaly.INCONSISTENT_DATA)
    is_dict = lambda field: type(field) is dict
    starts_with_www = lambda field: field.startswith('www.')

    inconsistenf_fields = list(filter(lambda result: result, [is_dict(visit.device), is_dict(visit.network),
                                                              is_dict(visit.browser), starts_with_www(visit.source)]))
    assert_that(inconsistenf_fields).is_length(2)

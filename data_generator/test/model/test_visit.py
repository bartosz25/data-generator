from assertpy import assert_that

from data_generator.model.entities import DataAnomaly
from data_generator.model.timer import Timer
from data_generator.model.visit import Visit


def should_create_visit_with_incomplete_data():
    visit = Visit(30, 'v1', DataAnomaly.INCOMPLETE_DATA, timer=Timer(-900), keep_private=False)

    incomplete_fields_candidates = [visit.visit_id, visit.user_id,
                                    visit.device, visit.network, visit.browser, visit.source]

    incomplete_fields = list(filter(lambda value: not value, incomplete_fields_candidates))

    assert_that(incomplete_fields).is_length(2)


def should_create_visit_with_inconsistent_data():
    visit = Visit(30, 'v1', DataAnomaly.INCONSISTENT_DATA, timer=Timer(-900), keep_private=False)
    def is_dict(field): return type(field) is dict
    def starts_with_www(field): return field.startswith('www.')

    inconsistenf_fields = list(filter(lambda result: result, [is_dict(visit.device), is_dict(visit.network),
                                                              is_dict(visit.browser), starts_with_www(visit.source)]))
    assert_that(inconsistenf_fields).is_length(2)

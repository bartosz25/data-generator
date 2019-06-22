from assertpy import assert_that

from data_generator.model import entities
from data_generator.model.visit import Visit


def should_generate_event_for_a_complete_visit():
    visit = Visit(30, 'v1', entities.DataAnomaly.INCOMPLETE_DATA)

    event_dict = entities.generate_event(visit)

    assert_that(event_dict).contains_key('source', 'page', 'user', 'visit_id', 'technical', 'event_time', 'user_id')
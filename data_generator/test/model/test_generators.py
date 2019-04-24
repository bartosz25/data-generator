from assertpy import assert_that

from model.entities import DataAnomaly
from model.generators import generate_visit_id, generate_user_id, generate_source
from visit import Visit

complete_visit = Visit(visit_duration=120, app_version='v1', data_anomaly=DataAnomaly.MISSING)


def should_generate_consistent_id_between_2_calls():
    visit_id_1 = generate_visit_id(complete_visit)
    visit_id_2 = generate_visit_id(complete_visit)

    assert_that(visit_id_1).is_equal_to(visit_id_2)


def should_generate_user_id_between_2_calls():
    user_id_1 = generate_user_id(complete_visit)
    user_id_2 = generate_user_id(complete_visit)

    assert_that(user_id_1).is_equal_to(user_id_2)


def should_generate_valid_source():
    source = generate_source(complete_visit)

    assert_that(source['site']).is_equal_to('mysite.com')
    assert_that(source['api_version']).is_equal_to('v1')

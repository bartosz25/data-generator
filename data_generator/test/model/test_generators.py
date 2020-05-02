from assertpy import assert_that

from data_generator.model.entities import DataAnomaly
from data_generator.model.generators import generate_visit_id, generate_user_id, generate_source, \
    generate_user_context, generate_technical_context, generate_event_time, generate_visited_page, \
    generate_keep_private_flag
from data_generator.model.timer import Timer
from data_generator.model.visit import Visit

complete_visit = Visit(visit_duration_seconds=120, app_version='v1', data_anomaly=DataAnomaly.MISSING,
                       timer=Timer(-900), keep_private=False)


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

    assert_that(source['site']).is_in('mysite.com', 'partner1.com', 'partner2.com', 'partner3.com', 'partner4.com',
                                      'partner5.com', 'partner6.com', 'partner7.com', 'partner8.com',
                                      'partner9.com', 'partner10.com')
    assert_that(source['api_version']).is_equal_to('v1')
    assert_that(source).contains_key('site', 'api_version')


def should_generate_valid_user_context():
    user_context = generate_user_context(complete_visit)

    assert_that(user_context['ip']).is_equal_to(complete_visit.ip)
    assert_that(user_context['latitude']).is_equal_to(complete_visit.latitude)
    assert_that(user_context['longitude']).is_equal_to(complete_visit.longitude)


def should_generate_valid_technical_context():
    technical_context = generate_technical_context(complete_visit)

    assert_that(technical_context['browser']).is_equal_to(complete_visit.browser)
    assert_that(technical_context['os']).is_equal_to(complete_visit.os)
    assert_that(technical_context['lang']).is_equal_to(complete_visit.language)
    assert_that(technical_context['device']).is_equal_to(
        {'type': complete_visit.device, 'version': complete_visit.device_version})
    assert_that(technical_context['network']).is_equal_to(complete_visit.network)


def should_generate_valid_event_time():
    event_time = generate_event_time(complete_visit)

    assert_that(event_time).matches(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00')


def should_generate_visited_page():
    visited_page = generate_visited_page(complete_visit)

    assert_that(visited_page).contains_key('previous', 'current')


def should_generate_immutable_keep_private_flag():
    keep_private_flag_1 = generate_keep_private_flag(complete_visit)
    keep_private_flag_2 = generate_keep_private_flag(complete_visit)

    assert_that(keep_private_flag_1).is_equal_to(keep_private_flag_2)

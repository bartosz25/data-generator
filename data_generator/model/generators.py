from datetime import datetime, timezone


def generate_visit_id(visit):
    return visit.visit_id


def generate_user_id(visit):
    return visit.user_id


def generate_visited_page(visit):
    return {'previous': visit.previous_page, 'current': visit.current_page}


def generate_source(visit):
    return {
        "site": visit.source,
        "api_version": visit.app_version
    }


def generate_user_context(visit):
    return {
        "ip": visit.ip,
        "latitude": visit.latitude,
        "longitude": visit.longitude
    }


def generate_technical_context(visit):
    # browser, os, lang, device, network type (wifi, lan)
    return {
        "browser": visit.browser,
        "os": visit.os,
        "lang": visit.language,
        "device": {"type": visit.device, "version": visit.device_version},
        "network": visit.network
    }


def generate_event_time(visit):
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

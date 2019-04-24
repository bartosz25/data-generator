from enum import Enum

from model import generators


def generate_event(visit):
    event_dict = {
        "visit_id": generators.generate_visit_id(visit),
        "event_time": generators.generate_event_time(visit),
        "user_id": generators.generate_user_id(visit),
        "page": generators.generate_visited_page(visit),
        "source": generators.generate_source(visit),
        "user": generators.generate_user_context(visit),
        "technical": generators.generate_technical_context(visit)
    }
    return event_dict


class DataAnomaly(Enum):
    MISSING = 1,
    INCOMPLETE_DATA = 2,
    INCONSISTENT_DATA = 3



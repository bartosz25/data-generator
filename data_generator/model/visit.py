import ipaddress
import json
import logging
import random
import uuid

from data_generator.model import entities
from data_generator.model.entities import DataAnomaly

logger = logging.getLogger('Visit')


def generate_ip():
    flag = random.randint(0, 1)
    if flag == 0:
        random_bits_integer = random.getrandbits(32)
        ip4_address = ipaddress.IPv4Address(random_bits_integer)
        return str(ip4_address)
    else:
        random_bits_integer = random.getrandbits(128)
        ip6_address = ipaddress.IPv6Address(random_bits_integer)
        return ip6_address.compressed


class Visit:
    def __init__(self, visit_duration_seconds, app_version, data_anomaly, timer, keep_private):
        """
        Entity class representing one user's visit on the website. In order to keep dataset distribution consistent
        after the visit's expiration, this class should be reused.Every time a visit expires, it should be reinitialized
        through :funct:`~data_generator.model.visit.Visit.reinitialize_visit`

        :param visit_duration_seconds:
        :param app_version: Version of the application associated to the visit.
        :param data_anomaly: The anomaly that will be applied on this visit.
        :param keep_private: A boolean flag saying whether user wants his personal data to be anonymized
        """
        self.app_version = app_version
        self.data_anomaly = data_anomaly
        self.timer = timer
        self.keep_private = keep_private
        self._reset_fields(visit_duration_seconds)

    def event_time(self):
        return self.next_action_time

    def get_remaining_session_time_in_sec(self):
        return self.generation_end_time - self.last_action

    def generate_new_action(self, pages_to_visit, duration, is_valid_log=True):
        if not self.current_page:
            possible_actions = pages_to_visit.keys()
        else:
            possible_actions = pages_to_visit[self.current_page]

        self.previous_page = self.current_page
        self.current_page = random.choice(list(possible_actions))

        json_data = json.dumps(entities.generate_event(self, is_valid_log))

        new_next_action_time = self.next_action_time + duration
        if new_next_action_time > self.generation_end_time:
            self.next_action_time = self.generation_end_time
            self.is_to_close = True
        else:
            self.next_action_time = new_next_action_time
            self.is_to_close = False

        return json_data

    def reinitialize_visit(self, new_duration):
        self._reset_fields(new_duration)
        return self

    def output_log_to_the_sink(self):
        return not self.is_to_close and self.next_action_time < self.timer.current_time()

    def _reset_fields(self, visit_duration):
        self.is_to_close = False
        self.next_action_time = self.timer.current_time()
        self.visit_id = uuid.uuid4().hex
        self.user_id = random.randint(1, 1000000)
        self.ip = generate_ip()
        self.longitude = round(random.uniform(-180, 180), 4)
        self.latitude = round(random.uniform(-90, 90), 4)
        self.duration_seconds = visit_duration
        self.generation_end_time = self.timer.current_time() + visit_duration
        # random weight ==> https://stackoverflow.com/questions/14992521/python-weighted-random
        source_sites = list(map(lambda site_id: "partner{}.com".format(site_id), range(1, 10))) + ["mysite.com"] * 90
        self.source = random.choice(source_sites)
        browsers = list(map(lambda version: "Google Chrome {}".format(version), range(55, 60))) + \
            list(map(lambda version: "Mozilla Firefox {}".format(version), range(51, 55))) + \
            list(map(lambda version: "Microsoft Edge {}".format(version), range(14, 15)))
        self.browser = random.choice(browsers)
        languages = ["fr", "pl", "de"] + ["en"] * 20
        self.language = random.choice(languages)
        devices = ["pc", "tablet", "smartphone"]
        self.device = random.choice(devices)
        networks = ["adsl", "fiber_optic", "3g", "4g"]
        self.network = random.choice(networks)

        operating_systems = {"pc": ["Ubuntu 16", "Ubuntu 18", "Windows 8", "Windows 10", "macOS 10.12", "macOS 10.13",
                                    "macOS 10.14"],
                             "tablet": ["Android 8.1", "Android 9.0", "iOS 9", "iOS 10", "iOS 11", "iOS 12"],
                             "smartphone": ["Android 8.1", "Android 9.0", "iOS 9", "iOS 10", "iOS 11", "iOS 12"]}
        self.os = random.choice(operating_systems[self.device])
        device_versions = {"tablet": {
            "android": ["Samsung Galaxy Tab S4", "Samsung Galaxy Tab S3"],
            "ios": ["iPad Pro 11", "iPad Pro 12.9", "iPad mini 4", "iPad Pro 10.5"]
        }, "smartphone": {
            "android": ["Samsung Galaxy Note 9", "Huawei Mate 20 Pro", "Google Pixel 3 XL", "Pixel 3",
                        "Huawei P20 Pro"],
            "ios": ["Apple iPhone XS", "Apple iPhone XR"]
        }}
        self.device_version = None
        if self.device != "pc":
            os_type = self.os.split(" ")[0].lower()
            eligible_versions = device_versions[self.device][os_type]
            self.device_version = random.choice(eligible_versions)

        self.current_page = None
        self.previous_page = None

        self.__apply_anomalies()

    def __apply_anomalies(self):
        anomaly_candidates = ['device', 'network', 'browser', 'source']
        properties_to_change = random.sample(anomaly_candidates, k=2)
        if self.data_anomaly == DataAnomaly.INCOMPLETE_DATA:
            for property_to_remove in properties_to_change:
                setattr(self, property_to_remove, None)
        elif self.data_anomaly == DataAnomaly.INCONSISTENT_DATA:
            for property_to_replace in properties_to_change:
                getattr(self, '_change_{}'.format(property_to_replace))()

    def _change_device(self):
        self.device = {'name': self.device}

    def _change_network(self):
        self.network = {'short_name': self.network[0:1], 'long_name': self.network}

    def _change_browser(self):
        self.browser = {'name': self.browser, 'language': self.language}
        self.language = None

    def _change_source(self):
        self.source = 'www.{}'.format(self.source)

    def __repr__(self):
        return 'Visit: {duration} seconds, {version}, {anomaly}'.format(duration=self.duration_seconds,
                                                                        version=self.app_version,
                                                                        anomaly=self.data_anomaly)

from random import shuffle, randrange

from data_generator.helper.percentage import calculate_value
from data_generator.model.entities import DataAnomaly
from data_generator.model.timer import Timer
from data_generator.model.visit import Visit


class Dataset():
    def __init__(self,
                 duration_min_seconds, duration_max_seconds,
                 percentage_incomplete_data, percentage_inconsistent_data,
                 percentage_app_v1, percentage_app_v2,
                 users_number, timer, no_data_consent_percentage):
        """

        :param duration_min_seconds: The min duration of the generated visits
        :param duration_max_seconds: The max duration of the generated visits
        :param percentage_incomplete_data:
        :param percentage_inconsistent_data:
        :param percentage_app_v1:
        :param percentage_app_v2:
        :param users_number: The number of all users to generate in the dataset
        :param timer: `~data_generator.model.timer.Timer` implementation to use
        """
        self.__duration_min = duration_min_seconds
        self.__duration_max = duration_max_seconds
        self.timer = timer

        percentage_app_v3 = (100 - percentage_app_v1 - percentage_app_v2)
        self.versions_to_distribute = self.create_versions_distribution(users_number,
                                                                        app_v1=percentage_app_v1,
                                                                        app_v2=percentage_app_v2,
                                                                        app_v3=percentage_app_v3)

        self.data_anomalies_distribution = \
            self.create_data_anomalies_distribution(users_number,
                                                    incomplete_data_percentage=percentage_incomplete_data,
                                                    inconsistent_data_percentage=percentage_inconsistent_data)
        self.consent_flags = self.create_keep_private_flags_distribution(users_number, no_data_consent_percentage)

        self.visits = self.create_initial_visits(users_number)
        self.pages = self.create_page_map()

    @staticmethod
    def create_page_map():
        all_categories = list(map(lambda index: 'category {}'.format(index), range(1, 26)))
        static_pages = ['index', 'about', 'my-account']
        pages_to_visit = {}
        for category in all_categories:
            all_articles = list(map(lambda index: 'article {}-{}'.format(category, index), range(1, 26)))
            pages_to_visit[category] = all_categories + static_pages + all_articles
            for article in all_articles:
                pages_to_visit[article] = all_categories + static_pages
        for static_page in static_pages:
            pages_to_visit[static_page] = static_pages + all_categories
        return pages_to_visit

    @staticmethod
    def create_versions_distribution(users_number, app_v1, app_v2, app_v3):
        versions_to_distribute = ['v1'] * calculate_value(users_number, app_v1) + \
                                 ['v2'] * calculate_value(users_number, app_v2) + \
                                 ['v3'] * calculate_value(users_number, app_v3)
        # remember - shuffle is in-place modification
        # https://stackoverflow.com/questions/12765219/nonetype-object-is-not-subscriptable-trying-to-create-the-monty-hall-theory  # noqa
        shuffle(versions_to_distribute)
        return versions_to_distribute

    @staticmethod
    def create_data_anomalies_distribution(users_number, incomplete_data_percentage,
                                           inconsistent_data_percentage):
        data_with_anomaly_percentage = incomplete_data_percentage + inconsistent_data_percentage
        data_anomalies_distribution = [DataAnomaly.MISSING] * calculate_value(users_number,
                                                                              100 - data_with_anomaly_percentage) + \
            [DataAnomaly.INCOMPLETE_DATA] * calculate_value(users_number,
                                                            incomplete_data_percentage) + \
            [DataAnomaly.INCONSISTENT_DATA] * calculate_value(users_number,
                                                              inconsistent_data_percentage)
        shuffle(data_anomalies_distribution)
        return data_anomalies_distribution

    @staticmethod
    def create_keep_private_flags_distribution(users_number, no_consent_users):
        no_data_consent_number = calculate_value(users_number, no_consent_users)
        consent_flags = [True] * no_data_consent_number + [False] * (users_number - no_data_consent_number)
        shuffle(consent_flags)
        return consent_flags

    def create_initial_visits(self, users_number):
        visits = []
        for user_id in range(0, users_number):
            visit_duration = randrange(self.__duration_min, self.__duration_max)
            visits.append(Visit(visit_duration_seconds=visit_duration, app_version=self.versions_to_distribute[user_id],
                                data_anomaly=self.data_anomalies_distribution[user_id], timer=self.timer,
                                keep_private=self.consent_flags[user_id]))

        return visits

    def reinitialize_visit(self, visit):
        visit.reinitialize_visit(new_duration=randrange(self.__duration_min, self.__duration_max))

    @staticmethod
    def from_yaml(configuration):
        dataset_configuration = configuration['dataset']
        versions_configuration = dataset_configuration['versions_percentage']
        duration_interval_configuration = dataset_configuration['session_duration_seconds']
        composition_configuration = dataset_configuration['composition_percentage']
        return Dataset(
            duration_min_seconds=duration_interval_configuration['min'],
            duration_max_seconds=duration_interval_configuration['max'],
            percentage_incomplete_data=composition_configuration['incomplete'],
            percentage_inconsistent_data=composition_configuration['inconsistent'],
            percentage_app_v1=versions_configuration['v1'],
            percentage_app_v2=versions_configuration['v2'],
            users_number=dataset_configuration['all_users'],
            timer=Timer(latency_seconds=dataset_configuration['real_time_delta_seconds']),
            no_data_consent_percentage=dataset_configuration['users_no_data_consent_percentage']
        )

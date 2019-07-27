from datetime import timedelta
from random import shuffle, randrange

from data_generator.helper.percentage import calculate_value
from data_generator.model.entities import DataAnomaly
from data_generator.model.visit import Visit


class Dataset():
    def __init__(self,
                 duration_min_seconds, duration_max_minutes,
                 percentage_incomplete_data, percentage_inconsistent_data,
                 percentage_app_v1, percentage_app_v2,
                 users_number, timer):
        self.__duration_min = timedelta(seconds=duration_min_seconds).total_seconds()
        self.__duration_max = timedelta(minutes=duration_max_minutes).total_seconds()
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

    def create_initial_visits(self, users_number):
        visits = []
        for user_id in range(0, users_number):
            visit_duration = randrange(self.__duration_min, self.__duration_max)
            visits.append(Visit(visit_duration_seconds=visit_duration, app_version=self.versions_to_distribute[user_id],
                                data_anomaly=self.data_anomalies_distribution[user_id], timer=self.timer))

        return visits

    def reinitialize_visit(self, visit):
        visit.reinitialize_visit(new_duration=randrange(self.__duration_min, self.__duration_max))

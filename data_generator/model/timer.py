import datetime


class Timer:
    """
    Timer idea is to facilitate latency simulation. For now it's an object shared by all the visits but if needed,
    it can be also parametrized at visit's level.
    """
    def __init__(self, latency_seconds):
        self.latency_seconds = latency_seconds

    def current_time(self):
        """
        :return: Number of milliseconds with defined latency. Take care of not specifying the timezone here because
                 it can lead to the incorrect output in JSON's "event_time" field which is formatted to the UTC.
                 For instance, if you change it to utcnow(), the UTC time for "event_time" will be computed as it
                 was your local timezone.
        """
        return int(int(datetime.datetime.now().timestamp()) + self.latency_seconds)

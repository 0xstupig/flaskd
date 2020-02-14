from datetime import datetime


class EventData(object):
    def __init__(self, **kwargs):
        self.timestamp = datetime.now()

    @classmethod
    def get_event_name(cls):
        return cls.__name__

    def get_data(self):
        return self.__dict__


class InvalidEventData(Exception):
    pass

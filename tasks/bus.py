from typing import Callable

from event_bus import EventBus

from tasks.model.base import EventData, InvalidEventData


class OverriddenEventBus(object):
    def __init__(self, event_bus: EventBus = None):
        self._instance = event_bus

    def init(self, event_bus: EventBus = None):
        self._instance = event_bus

    def trigger(self, event, sync=False):
        if not issubclass(event.__class__, EventData):
            raise InvalidEventData()

        if self._instance is None:
            return

        event_key = event.get_event_name()

        if sync:
            self._instance.emit(event_key, event)
        else:
            self._instance.emit(event_key, event, threads=True)

    def register(self, event_cls, functions: set):  # Type: Set[Callable]
        if not issubclass(event_cls, EventData):
            raise InvalidEventData()

        if self._instance is None:
            return

        for func in functions:
            if isinstance(func.__class__, Callable):
                self._instance.add_event(func, event_cls.get_event_name())


bus = OverriddenEventBus()


class NullEventBus(object):
    Instance = bus


class DefaultEventBus(object):
    Instance = bus

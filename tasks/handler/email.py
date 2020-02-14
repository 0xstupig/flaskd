from tasks.model.email import IncomingRegistrationEventData
from tasks.worker.email import incoming_registration_notify


class IncomingRegistrationEventHandler(object):
    @classmethod
    def handle_event(cls, event: IncomingRegistrationEventData):
        incoming_registration_notify.delay(**event.get_data())

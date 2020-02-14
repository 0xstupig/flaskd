from tasks.model.base import EventData


class IncomingRegistrationEventData(EventData):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.record_id = kwargs.pop('record_id')
        self.restaurant_name = kwargs.pop('restaurant_name')
        self.owner_name = kwargs.pop('owner_name')
        self.email = kwargs.pop('email')
        self.status = kwargs.pop('status')
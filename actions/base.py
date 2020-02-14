from models import db
from tasks import bus


class BaseAction:
    def __init__(self, **kwargs):
        self.db = kwargs.pop('db', db)
        self.model = kwargs.pop('model', self.db.Model)
        self.bus = kwargs.pop('bus', bus)

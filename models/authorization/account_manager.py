from models import db
from models.base import UserMixin, SuspendMixin
from models.authorization.base_user import BaseUser


class AccountManager(BaseUser, UserMixin, SuspendMixin):
    __tablename__ = 'account_managers'

    id = db.Column(db.BigInteger, db.ForeignKey('base_users.id'), primary_key=True, autoincrement=False)

    restaurant_id = db.Column(db.BigInteger, db.ForeignKey('restaurants.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'manager',
    }

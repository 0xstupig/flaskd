from enum import Enum

from models import db
from models.base import UserMixin, SuspendMixin
from models.authorization.base_user import BaseUser

user_cuisines = db.Table(
    'user_cuisines',
    db.Column('cuisine_id', db.BigInteger, db.ForeignKey('cuisines.id'), primary_key=True),
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
)

user_types = db.Table(
    'user_types',
    db.Column('type_id', db.BigInteger, db.ForeignKey('restaurant_types.id'), primary_key=True),
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
)

user_ingredients = db.Table(
    'user_ingredients',
    db.Column('ingredient_id', db.BigInteger, db.ForeignKey('ingredients.id'), primary_key=True),
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
)

user_allergies = db.Table(
    'user_allergies',
    db.Column('allergy_id', db.BigInteger, db.ForeignKey('allergies.id'), primary_key=True),
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
)

following_collections = db.Table(
    'following_collections',
    db.Column('collection_id', db.BigInteger, db.ForeignKey('collections.id'), primary_key=True),
    db.Column('user_id', db.BigInteger, db.ForeignKey('users.id'), primary_key=True)
)


class Gender(Enum):
    FEMALE = 1
    MALE = 2
    OTHER = 3


class User(BaseUser, UserMixin, SuspendMixin):
    __tablename__ = 'users'

    __mapper_args__ = {
        'polymorphic_identity': 'user',
    }

    id = db.Column(db.BigInteger, db.ForeignKey('base_users.id'), primary_key=True, autoincrement=False)

    facebook_id = db.Column(db.String(128), nullable=True)
    google_id = db.Column(db.String(128), nullable=True)

    birthday = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.Enum(Gender), nullable=True)
    city = db.Column(db.String(256), nullable=True)



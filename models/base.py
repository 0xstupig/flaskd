from datetime import datetime

import bcrypt
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Query, Mapper
from sqlalchemy.sql import expression

from models.id_worker import IdWorker
from utilities.constant import machine_id, PASSWORD_ENCODING
from utilities.exception import EntityNotFoundException
from utilities.helper import Utility


class Base(Model):
    def __repr__(self):
        return '<{} with {}>'.format(self.__tablename__, self.id)

    def update(self, value):
        for k, v in value.items():
            if k != 'id':
                setattr(self, k, v)


class BaseQuery(Query):
    def _get_models(self, query):
        if hasattr(query, 'attr'):
            return query.attr.target_mapper
        else:
            return Utility.first_or_none(
                [d['expr'].class_ for d in query.column_descriptions if isinstance(d['expr'], Mapper)])

    def active(self):
        model_class = self._get_models(self)
        if model_class:
            if hasattr(model_class, 'is_active'):
                return self.filter(model_class.is_active == expression.true())

        return self

    def not_deleted(self):
        model_class = self._get_models(self)
        if model_class:
            if hasattr(model_class, 'is_deleted'):
                return self.filter(model_class.is_deleted == expression.false())

        return self

    def get_or_404(self, id_, ignore_soft_delete=False):
        entity = self.get(id_)
        not_found = False
        model_class = self._get_models(self)

        if not entity:
            not_found = True

        if not ignore_soft_delete:
            if hasattr(model_class, 'is_deleted'):
                not_found = entity.is_deleted == True

            if hasattr(model_class, 'is_active') and not not_found:
                not_found = entity.is_active == False

        if not_found:
            raise EntityNotFoundException(id_, model_class.__tablename__)

        return entity


db = SQLAlchemy(model_class=Base, query_class=BaseQuery)
id_handler = IdWorker(machine_id())


class IdMixin(object):
    id = db.Column(db.BigInteger, primary_key=True)


class DistributeIdMixin(object):
    id = db.Column(db.BigInteger, primary_key=True)

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', id_handler.next_id())


class CreationTimeMixin(object):
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)


class ModificationTimeMixin(object):
    modification_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PassivableMixin(object):
    is_active = db.Column(db.Boolean, unique=False, default=True, server_default=expression.true())


class SoftDeleteMixin(object):
    is_deleted = db.Column(db.Boolean, unique=False, default=False, server_default=expression.false())


class SuspendMixin(object):
    is_suspended = db.Column(db.Boolean, unique=False, default=False, server_default=expression.false())


class UserMixin(object):
    email = db.Column(db.String(50), unique=True)
    _password = db.Column('password', db.String(128))
    full_name = db.Column(db.String(128))
    phone_number = db.Column(db.String(20))
    avatar = db.Column(db.String(256))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt()).decode('utf8')

    def verify_password(self, password):
        if self.password is None:
            return False

        return bcrypt.checkpw(password.encode(PASSWORD_ENCODING), self.password.encode(PASSWORD_ENCODING))


class ModificationUserMixin(object):
    updated_by = db.Column(db.BigInteger)


class CreationUserMixin(object):
    created_by = db.Column(db.BigInteger)

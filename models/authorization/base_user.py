from models import db

from models.base import CreationTimeMixin, ModificationTimeMixin, DistributeIdMixin
from models.authorization.reset_token import ResetToken
from models.authorization.session import Session
from models.authorization.role import Role


class BaseUser(db.Model, DistributeIdMixin, CreationTimeMixin, ModificationTimeMixin):
    __tablename__ = 'base_users'
    
    type = db.Column(db.String)

    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id'))
    role = db.relationship(Role, uselist=False, lazy='joined')
    
    sessions = db.relationship(Session, backref='user', lazy=True)
    reset_token = db.relationship(ResetToken, backref='user', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'base_user',
        'polymorphic_on': type
    }

    def __init__(self, **kwargs):
        DistributeIdMixin.__init__(self, **kwargs)
        super().__init__(**kwargs)

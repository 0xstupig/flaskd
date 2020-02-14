from models import db
from models.base import IdMixin, CreationTimeMixin, ModificationTimeMixin


class ResetToken(db.Model, IdMixin, CreationTimeMixin, ModificationTimeMixin):
    __tablename__ = 'reset_tokens'

    token = db.Column(db.String(6), unique=True, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('base_users.id'), nullable=False)
    expire = db.Column(db.DateTime, nullable=False)

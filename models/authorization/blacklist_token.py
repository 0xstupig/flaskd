from models import db

from models.base import IdMixin, CreationTimeMixin, ModificationTimeMixin


class BlacklistToken(db.Model, IdMixin, CreationTimeMixin, ModificationTimeMixin):
    __tablename__ = 'blacklist_tokens'

    token_id = db.Column(db.String(32), unique=True, nullable=False)

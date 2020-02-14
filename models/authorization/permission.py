from models import db
from models.base import IdMixin, ModificationTimeMixin, CreationTimeMixin


class Permission(db.Model, IdMixin, CreationTimeMixin, ModificationTimeMixin):
    __tablename__ = 'permissions'
    
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    display_name = db.Column(db.String(128), nullable=False, default='')
    parent_id = db.Column(db.BigInteger, db.ForeignKey('permissions.id'), nullable=True, default=None)

    parent = db.relationship('Permission', remote_side='Permission.id', backref='sub_permissions')

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property

from models import db
from models.authorization.permission import Permission
from models.base import IdMixin, CreationTimeMixin, ModificationTimeMixin


class Role(db.Model, IdMixin, CreationTimeMixin, ModificationTimeMixin):
    __tablename__ = 'roles'

    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    display_name = db.Column(db.String(128), nullable=False, default='')

    permissions = association_proxy('role_permissions', 'permission',
                                    creator=lambda permission: RolePermission(permission=permission))

    @hybrid_property
    def permission_names(self):
        return [permission.name for permission in self.permissions]

    @classmethod
    def get_role_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_roles_by_names(cls, names):
        return cls.query.filter(cls.name.in_(names)).all()


class RolePermission(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.BigInteger, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.BigInteger, db.ForeignKey('permissions.id'), primary_key=True)

    role = db.relationship('Role', backref=db.backref('role_permissions', cascade='all, delete-orphan', lazy='joined'))
    permission = db.relationship(Permission, lazy='joined')

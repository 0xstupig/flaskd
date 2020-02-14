from enum import Enum, unique

from actions.base import BaseAction
from models.authorization.role import Role, Permission
from schemas.permission import permission_schemas
from schemas.role import RoleSchema


@unique
class ROLE(Enum):
    HostAdmin = 'HostAdmin'
    HostSupportAdmin = 'HostSupportAdmin'
    Consumer = 'Consumer'


class RoleAction(BaseAction):
    def __init__(self, model):
        super().__init__(model=model)
        self.roles = {}

    def init_app(self, app):
        with app.app_context():
            self.update_roles()

    def update_roles(self):
        self.roles = {}
        role_schema = RoleSchema(exclude=['permissions'])

        role_entities = Role.query.all()
        for role_entity in role_entities:
            role_data = role_schema.dump(role_entity)
            role_data['permissions'] = {
                permission['name']: permission
                for permission in permission_schemas.dump(role_entity.permissions)
            }

            self.roles[role_entity.name] = role_data

    def has_permission(self, role_name, permission_names):
        if role_name not in self.roles:
            return False

        role = self.roles[role_name]
        intersection = set(role['permissions']).intersection(permission_names)
        return len(intersection) == len(permission_names)

    def get_all(self):
        return list(Role.query.all())

    def create(self, data):
        role = Role(**data)
        self.db.session.add(role)
        self.db.session.commit()
        self.update_roles()

        return role

    def update_permissions(self, role_id, data):
        role = Role.query.get_or_404(role_id)
        if 'permissions' in data:
            permissions = sorted(data['permissions'])
            role.permissions = []

            for permission_id in permissions:
                permission = Permission.query.get_or_404(permission_id)
                role.permissions.append(permission)

                if permission.parent is None:
                    role.permissions.extend(permission.sub_permissions)
        else:
            return False

        self.db.session.commit()
        self.update_roles()

        return role

    def delete(self, role_id):
        role = Role.query.get_or_404(role_id)

        self.db.session.delete(role)
        self.db.session.commit()
        self.update_roles()


role_action = RoleAction(model=Role)

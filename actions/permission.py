from flask import g

from actions.base import BaseAction
from actions.role import role_action
from models.authorization import Permission, BaseUser


class PermissionAction(BaseAction):
    def __init__(self, model, action):
        super().__init__(model=model)
        self.role_action = action

    def get_all(self):
        return list(Permission.query.all())

    def create(self, data):
        permission = Permission(**data)
        self.db.session.add(permission)
        self.db.session.commit()
        return permission

    def delete(self, permission_id):
        permission = Permission.query.get_or_404(permission_id)

        self.db.session.delete(permission)
        self.db.session.commit()

    def is_granted(self, permission_names, user_id=None):
        if user_id:
            user = BaseUser.query.get_or_404(user_id)
            intersection = set(user.role.permission_names).intersection(permission_names)
            return len(intersection) == len(permission_names)

        role = g.payload.get('custom:role')

        return self.role_action.has_permission(role, permission_names)


permission_action = PermissionAction(Permission, action=role_action)

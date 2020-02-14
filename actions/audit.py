from actions.base import BaseAction
from models.audit import AuditLog


class AuditAction(BaseAction):
    def list(self, entity_id=None, entity_type=None, user_id=None, action=None, from_date=None, to_date=None,
             limit=100, offset=0):
        query = AuditLog.query
        if entity_type:
            query = query.filter_by(entity_type=entity_type)
            if entity_id:
                query = query.filter_by(entity_id=entity_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if action:
            query = query.filter_by(action=action)
        if from_date:
            query = query.filter(AuditLog.creation_date > from_date)
        if to_date:
            query = query.filter(AuditLog.creation_date < to_date)

        return query[offset:offset+limit], query.count()


audit_action = AuditAction(model=AuditLog)


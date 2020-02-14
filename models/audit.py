import json

from sqlalchemy import event, inspect

from models.authorization import User
from models.base import CreationTimeMixin, IdMixin, db


class AuditLog(IdMixin, CreationTimeMixin, db.Model):
    __tablename__ = 'audit_logs'

    entity_id = db.Column(db.BigInteger)
    entity_type = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('base_users.id'), nullable=True)
    old_value = db.Column(db.String)
    new_value = db.Column(db.String)

    user = db.relationship('User', lazy=True)


AUDIT_CONFIG = {
    User: {
        'create': True,
        'update': True,
    }}


def _is_audit(type, action):
    if type not in AUDIT_CONFIG:
        return False

    return AUDIT_CONFIG[type].get(action, False)


def _get_id(obj):
    insp = inspect(obj)
    if insp.identity and len(insp.identity) == 1:
        return insp.identity

    return None


def _get_current_value(obj):
    current_value = {}

    insp = inspect(obj)
    for column_name in insp.mapper.columns.keys():
        current_value[column_name] = getattr(obj, column_name)

    return current_value


def _has_changes(obj):
    insp = inspect(obj)
    for column_name in insp.mapper.columns.keys():
        attr = getattr(insp.attrs, column_name)
        if attr.history.has_changes():
            return True

    return False


def _get_old_value(obj):
    old_value = {}

    insp = inspect(obj)
    for column_name, column in insp.mapper.columns.items():
        attribute = getattr(insp.attrs, column_name)

        addition, un_change, deletion = attribute.load_history()
        if deletion:
            old_value[column.key] = deletion[0]
        elif un_change:
            old_value[column.key] = un_change[0]

    return old_value


@event.listens_for(db.session, 'before_flush')
def _handle_before_flush(session, *args, **kwargs):
    user_id = session.info.get('user_id')

    for obj in session.dirty:
        obj_type = type(obj)
        if not _is_audit(obj_type, 'update'):
            continue

        if _has_changes(obj):
            old_value = _get_old_value(obj)
            new_value = _get_current_value(obj)
            entity_id = _get_id(obj)
            audit_log = AuditLog(
                entity_type=obj_type.__name__,
                entity_id=entity_id,
                action='update',
                user_id=user_id,
                new_value=json.dumps(new_value, sort_keys=True, default=str),
                old_value=json.dumps(old_value, sort_keys=True, default=str)
            )
            session.add(audit_log)
            pass

    for obj in session.deleted:
        obj_type = type(obj)
        if not _is_audit(obj_type, 'delete'):
            continue

        old_value = _get_old_value(obj)
        entity_id = _get_id(obj)
        audit_log = AuditLog(
            entity_type=obj_type.__name__,
            entity_id=entity_id,
            action='delete',
            user_id=user_id,
            old_value=json.dumps(old_value, sort_keys=True, default=str)
        )
        session.add(audit_log)
        pass

    pass


@event.listens_for(db.session, 'after_flush')
def _handle_after_flush(session, *args, **kwargs):
    user_id = session.info.get('user_id')

    for obj in session.new:
        if isinstance(obj, AuditLog):
            continue

        obj_type = type(obj)
        if not _is_audit(obj_type, 'create'):
            continue

        new_value = _get_current_value(obj)
        entity_id = _get_id(obj)
        audit_log = AuditLog(
            entity_type=obj_type.__name__,
            entity_id=entity_id,
            action='create',
            user_id=user_id,
            new_value=json.dumps(new_value, sort_keys=True, default=str)
        )
        session.add(audit_log)
        pass

    pass

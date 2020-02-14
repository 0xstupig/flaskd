import json

from marshmallow import fields

from schemas.base import IdSchema


class JsonField(fields.Field):
    def _serialize(self, value, attr, obj):
        if not value:
            return self.default

        return json.loads(value)

    def _deserialize(self, value, attr, data):
        if not value:
            return self.missing

        return json.dumps(value)


class AuditLogSchema(IdSchema):
    entity_id = fields.Integer()
    entity_type = fields.String()
    user_id = fields.String()
    action = fields.String()
    old_value = JsonField()
    new_value = JsonField()
    creation_date = fields.DateTime()


audit_log_schema = AuditLogSchema()
audit_log_schemas = AuditLogSchema(many=True)
from marshmallow import Schema, fields


class ListAuditLogRequestSchema(Schema):
    user_id = fields.String()
    user_entity = fields.Integer()
    action = fields.Integer()
    from_date = fields.DateTime()
    to_date = fields.DateTime()
    limit = fields.Integer(default=100)
    offset = fields.Integer(default=0)


list_audit_log_request_schema = ListAuditLogRequestSchema()

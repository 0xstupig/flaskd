from marshmallow import Schema, ValidationError, fields, post_load, \
    validates, pre_dump

from utilities.helper import Utility


class DistributeIdSchema(Schema):
    id = fields.String(allow_none=True, allow_empty=True)


class IdSchema(Schema):
    id = fields.Integer(allow_none=True)


class PassivableSchema(Schema):
    is_active = fields.Boolean()



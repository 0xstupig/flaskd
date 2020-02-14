from marshmallow import EXCLUDE, fields

from schemas.base import IdSchema


class PermissionSchema(IdSchema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)
    description = fields.String()
    display_name = fields.String()
    parent_id = fields.Integer()


permission_schema = PermissionSchema()
permission_schemas = PermissionSchema(many=True)

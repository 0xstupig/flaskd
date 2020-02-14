from marshmallow import fields, EXCLUDE, Schema, validates_schema, ValidationError
from marshmallow_enum import EnumField

from models.authorization.user import User, Gender
from schemas.base import DistributeIdSchema
from schemas.role import RoleSchema


class UserSchema(DistributeIdSchema):
    __model__ = User

    class Meta:
        unknown = EXCLUDE

    email = fields.Email(required=True)
    password = fields.String(load_only=True)
    role_id = fields.Integer(required=True)
    avatar = fields.String()

    birthday = fields.DateTime()
    city = fields.String()
    gender = EnumField(Gender, by_value=True)

    facebook_id = fields.String()
    google_id = fields.String()

    full_name = fields.String(required=True)
    phone_number = fields.String()


class UserProfileSchema(DistributeIdSchema):
    email = fields.Email()
    role_id = fields.Integer(dump_only=True)
    avatar = fields.String()

    birthday = fields.DateTime()
    city = fields.String()
    gender = EnumField(Gender, by_value=True)

    facebook_id = fields.String()
    google_id = fields.String()

    full_name = fields.String()
    phone_number = fields.String()
    role = fields.Nested(RoleSchema, dump_only=True)


class UserCredentialPostSchema(Schema):
    password = fields.String(allow_none=False)
    update_password = fields.String(allow_none=False)

    @validates_schema
    def validate_password(self, data):
        if data['password'] == data['update_password']:
            raise ValidationError('Update password must different with current password.')


user_review_schema = UserSchema(only=['email', 'full_name', 'avatar'])
user_response_schema = UserSchema(exclude=['facebook_id', 'google_id'])
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_profile_schema = UserProfileSchema()
user_credential_post_schema = UserCredentialPostSchema()

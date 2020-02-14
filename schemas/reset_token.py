from marshmallow import Schema, fields, EXCLUDE, post_load
from models.authorization.reset_token import ResetToken


class ResetTokenSchema(Schema):
    __model_ = ResetToken

    class Meta:
        unknown = EXCLUDE

    token = fields.String(required=True)
    user_id = fields.String()
    expire = fields.DateTime()

    @post_load
    def make_user(self, data):
        return ResetToken(**data)

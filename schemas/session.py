from marshmallow import EXCLUDE, fields, post_load
from models.authorization.session import Session
from schemas.base import IdSchema


class SessionSchema(IdSchema):
    __model_ = Session

    class Meta:
        unknown = EXCLUDE

    token = fields.String(required=True)

    @post_load
    def make_user(self, data):
        return Session(**data)


session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

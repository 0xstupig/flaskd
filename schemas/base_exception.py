from marshmallow import fields, Schema, post_load

from utilities.exception import BaseException_


class BaseExceptionSchema(Schema):
    __model__ = BaseException_

    message = fields.String()
    status_code = fields.Integer()

    @post_load
    def make_object(self, data):
        return self.__model__(**data)


gem_base_exception_return_schema = BaseExceptionSchema(only=['message', 'status_code'])

from urllib.parse import unquote

from marshmallow import Schema, fields, pre_load
from marshmallow_enum import EnumField

from utilities.constant import DEFAULT_LANGUAGE
from utilities.enum import SortDirection
from utilities.helper import Utility


class RequestSchema(Schema):
    @pre_load
    def set_default_to_none(self, data):
        for key, value in data.items():
            if value is None:
                data[key] = self.fields[key].default

            # TODO: must check field type before convert to int
            data[key] = int(value) if Utility.can_represents_int(value) else value

        return data


class SortRequestSchema(Schema):
    sort = fields.Boolean(default=None, allow_none=True)
    direction = EnumField(enum=SortDirection, default=SortDirection.ASC, by_value=True, allow_none=True)


class GeoRequestSchema(Schema):
    geo = fields.String(allow_none=True, allow_empty=True)


class PaginationSchema(Schema):
    limit = fields.Integer(default=10, allow_none=True)
    offset = fields.Integer(default=0, allow_none=True)


class MediaPaginationSchema(Schema):
    limit = fields.Integer(default=10)
    page = fields.Integer(default=1)


class I18nRequestSchema(Schema):
    language = fields.String(default=DEFAULT_LANGUAGE)
    all_language = fields.Boolean(default=False, allow_none=True)


class PassivableRequestSchema(Schema):
    is_active = fields.Boolean(default=None, allow_none=True, missing=None)


class QueryStringRequestSchema(Schema):
    # TODO: Mask as required field
    q = fields.String(default='')

    @pre_load
    def clean_object(self, data):
        if 'q' in data:
            q = data['q']
            data['q'] = unquote(q) if q else q

        return data


class OrderRequestSchema(Schema):
    order_by = fields.String(default='')

    @pre_load
    def clean_object(self, data):
        if 'order_by' in data:
            order_by = data['order_by']
            data['order_by'] = unquote(order_by) if order_by else order_by

        return data


class MetadataRequestSchema(RequestSchema):
    slug = fields.String(default='')
    language = fields.String(default='en')


metadata_request_schema = MetadataRequestSchema()


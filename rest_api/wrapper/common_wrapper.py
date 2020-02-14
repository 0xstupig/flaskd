import json

from flask import Response


class SuccessResponse(Response):
    def __init__(self, data, status_code):
        super(SuccessResponse, self).__init__(
            response=json.dumps(
                {
                    'success': True,
                    'data': data
                },
                ensure_ascii=False).encode('utf8'),
            mimetype='application/json',
            content_type='application/json; charset=utf-8',
            status=status_code
        )


class GeneralResponse(Response):
    def __init__(self, success, data, status_code, msg=''):
        super(GeneralResponse, self).__init__(
            response=json.dumps(
                {
                    'success': success,
                    'message': msg,
                    'data': data
                },
                ensure_ascii=False).encode('utf8'),
            mimetype='application/json',
            content_type='application/json; charset=utf-8',
            status=status_code
        )


class PagingResponse(SuccessResponse):
    def __init__(self, items, total, **kwargs):
        data = {
            'items': items,
            'total': total,
        }

        if 'aggregations' in kwargs:
            data['aggregations'] = kwargs['aggregations']

        super(PagingResponse, self).__init__(
            data=data,
            status_code=200
        )

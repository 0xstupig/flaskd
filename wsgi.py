import json

from flask import request, Response, g
from flask_compress import Compress
from marshmallow import ValidationError

import actions
import models
import rest_api
import services
import tasks
from factory import create_app
from utilities.constant import config_env, DEFAULT_LANGUAGE
from utilities.exception import EntityNotFoundException, DuplicateException, ForbiddenException, \
    BadRequestException, UnauthorizedException, MissingFieldException, InternalServerException, \
    InvalidRefreshTokenException
from utilities.helper import Utility

compress = Compress()

app = create_app(__name__, config_env())
compress.init_app(app)
rest_api.init_app(app)
services.init_app(app, models.db)
actions.init_app(app)
tasks.init_app(app)


@app.route('/', methods=['GET'])
def health_check():
    return Response(json.dumps({'message': 'OK'}), mimetype='application/json', status=200)


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return handle_exception(BadRequestException(detail={**e.messages}))


@app.errorhandler(UnauthorizedException)
@app.errorhandler(ForbiddenException)
@app.errorhandler(BadRequestException)
@app.errorhandler(MissingFieldException)
@app.errorhandler(EntityNotFoundException)
@app.errorhandler(DuplicateException)
@app.errorhandler(InternalServerException)
@app.errorhandler(InvalidRefreshTokenException)
def handle_exception(e):
    return Response(json.dumps(e.to_dict()),  mimetype='application/json', status=e.status_code)


@app.before_request
def before_request():
    header_format = '{}-{}'
    prefix = app.config['HEADER_PREFIX']
    g.language = request.headers.get(header_format.format(prefix, 'Language'), DEFAULT_LANGUAGE)

    all_language = request.headers.get(header_format.format(prefix, 'All-Language'), False)
    g.all_language = Utility.safe_bool(all_language)



@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = \
            'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers

    return response


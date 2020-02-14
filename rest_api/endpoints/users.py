from flask import Blueprint, g, request
from marshmallow import ValidationError

from actions.user import user_action
from rest_api.decorators import is_authenticated
from rest_api.wrapper import SuccessResponse
from schemas.user import user_profile_schema, user_credential_post_schema

user_ctrl = Blueprint(name='user_ctrl', import_name=__name__, url_prefix='/users')


@user_ctrl.route('/_profile', methods=['GET'])
@is_authenticated
def get_user_profile():
    user_id = g.payload['sub']
    profile = user_action.get_user_profile(user_id)

    return SuccessResponse(profile, 200)


@user_ctrl.route('/_credentials', methods=['PUT'])
@is_authenticated
def update_user_credentials():
    user_id = g.payload['sub']
    validated_json = user_credential_post_schema.load(request.get_json())
    user_action.update_credential(user_id, **validated_json)

    return SuccessResponse({}, 200)


@user_ctrl.route('', methods=['PUT'])
@is_authenticated
def update_user_profile():
    user_id = g.payload['sub']
    data = request.get_json()
    validate_data = user_profile_schema.load(data)

    user = user_action.update(user_id=user_id, value=validate_data)

    return SuccessResponse(user, 200)


@user_ctrl.route('/_thumbnail', methods=['PUT'])
@is_authenticated
def update_user_thumbnail():
    user_id = g.payload['sub']
    files = request.files.getlist('file')

    if not files or len(files) <= 0:
        raise ValidationError('Missing thumbnail')

    thumbnail = user_action.upload_user_profile(user_id=user_id, file=files[0])
    user_action.update(user_id, {'avatar': thumbnail})

    return SuccessResponse(thumbnail, 200)


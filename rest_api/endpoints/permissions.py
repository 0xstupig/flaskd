from flask import Blueprint, request

from actions.permission import permission_action
from rest_api.decorators import is_authenticated, is_authorized
from rest_api.wrapper import SuccessResponse
from schemas.permission import permission_schema, permission_schemas

permission_ctrl = Blueprint(name='permission_ctrl', import_name=__name__, url_prefix='/permissions')


@permission_ctrl.route('', methods=['POST'])
@is_authenticated
@is_authorized(['PermissionManagement.Create'])
def create():
    data = request.get_json()
    validate_data = permission_schema.load(data)
    permission = permission_action.create(validate_data)
    result = permission_schema.dump(permission)

    return SuccessResponse(result, 200)


@permission_ctrl.route('', methods=['GET'])
@is_authenticated
@is_authorized(['PermissionManagement.GetAll'])
def get_all():
    permissions = permission_action.get_all()
    result = permission_schemas.dump(permissions)

    return SuccessResponse(result, 200)


@permission_ctrl.route('/<permission_id>', methods=['DELETE'])
@is_authenticated
@is_authorized(['PermissionManagement.Delete'])
def delete(permission_id):
    permission_action.delete(permission_id)

    return SuccessResponse(None, 200)

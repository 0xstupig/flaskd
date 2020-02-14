from flask import Blueprint, request

from actions.audit import audit_action
from rest_api.wrapper import PagingResponse
from schemas.audit_log import audit_log_schemas
from schemas.list_audit_log_request import list_audit_log_request_schema

audit_ctrl = Blueprint(name='audit_ctrl', import_name=__name__, url_prefix='/audit_log')


@audit_ctrl.route('', methods=['GET'])
def list_audit_log():
    query = list_audit_log_request_schema.load(request.args)
    audit_logs, count = audit_action.list(**query)
    return PagingResponse(audit_log_schemas.dump(audit_logs), count)

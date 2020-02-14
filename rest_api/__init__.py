import rest_api.swagger as swagger
from rest_api.endpoints.audit import audit_ctrl
from rest_api.endpoints.auth import auth_ctrl
from rest_api.endpoints.permissions import permission_ctrl
from rest_api.endpoints.users import user_ctrl


def init_app(app):
    app.register_blueprint(auth_ctrl)
    app.register_blueprint(audit_ctrl)
    app.register_blueprint(user_ctrl)
    app.register_blueprint(permission_ctrl)

    if app.config['API_DOCS']:
        swagger.init_app(app)

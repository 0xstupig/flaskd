from flasgger import Swagger

from os import path


def init_app(app):
    with app.app_context():
        Swagger(app, template_file=path.join(path.abspath(path.dirname(__file__)), 'index.yaml'))

from flask import Flask

import models
from config import config


def create_app(name, config_name):
    app = Flask(name)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    models.init_app(app)

    return app

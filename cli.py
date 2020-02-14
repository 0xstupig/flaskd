import models
import services
import commands

from factory import create_app
from utilities.constant import config_env

app = create_app(__name__, config_env())

services.init_app(app, models.db)
commands.init_app(app)

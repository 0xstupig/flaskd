from flask_migrate import Migrate

import services
from factory import create_app
from models.base import db

from models.authorization import *

app = create_app(__name__, config_name='migration')
services.init_app(app, db)

flask_migrate = Migrate(app, db, compare_type=True)

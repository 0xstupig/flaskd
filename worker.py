import services
from factory import create_app
from models import db
from tasks.queue import queue
import actions
from utilities.constant import config_env

app = create_app(__name__, config_env())
queue.init_app(app)
services.init_app(app, db)
actions.init_app(app)
celery = queue.celery

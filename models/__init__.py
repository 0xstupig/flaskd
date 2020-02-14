from models.base import db


def init_app(app):
    db.init_app(app)
    # James: This block of code only run as start server. do not run it on db migration or upgrade
    if app.import_name == 'wsgi':
        with app.app_context():
            db.metadata.create_all(db.engine)

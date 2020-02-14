from celery import Celery


class FlaskCelery(object):
    def __init__(self, app=None):
        self.celery = Celery()

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.celery = self._make_celery(app)

    def _make_celery(self, app):
        celery_ = Celery(app.import_name, broker=app.config['BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
        celery_.conf.update(app.config)

        class ContextClass(celery_.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_.Task = ContextClass

        return celery_


queue = FlaskCelery()



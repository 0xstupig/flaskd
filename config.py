import os

import sentry_sdk
from dotenv import load_dotenv
from sentry_sdk.integrations.flask import FlaskIntegration

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql:///flaskd'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
    SQLALCHEMY_ECHO = False

    ES_HOST = os.environ.get('ES_HOST') or 'localhost'
    ES_PORT = int(os.environ.get('ES_PORT', '9200'))
    ES_USE_SSL = os.environ.get('ES_USE_SSL', 'FALSE') == 'TRUE'

    JWT_SECRET = os.environ.get('JWT_SECRET') or 'you-never-guess'
    JWT_EXPIRE = os.environ.get('JWT_EXPIRE') or 86400 * 10

    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY') or 'you-never-guess'

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 587
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') or False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your@email.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'you-never-guess'
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your.default@email.com'

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    DEFAULT_PASSWORD = os.environ.get('DEFAULT_PASSWORD') or 'your-default-password'

    BROKER_URL = os.environ.get('BROKER_URL') or 'amqp://'
    CELERY_TASK_RESULT_EXPIRES = 30
    CELERY_TIMEZONE = os.environ.get('CELERY_TIMEZONE') or 'UTC'
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'rpc://'

    COMPRESS_MIMETYPES = ['application/json']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SWAGGER = {'uiversion': 3}
    API_DOCS = os.environ.get('API_DOCS')


class ProductionConfig(Config):
    DEBUG = False
    API_DOCS = os.environ.get('API_DOCS')
    SWAGGER = {'uiversion': 3}

    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    SENTRY_ENV = os.environ.get('SENTRY_ENV')

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        sentry_sdk.init(dsn=app.config['SENTRY_DSN'], environment=app.config['SENTRY_ENV'],
                        integrations=[FlaskIntegration()])


class MigrationConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'migration': MigrationConfig
}

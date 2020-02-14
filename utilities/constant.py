import ipaddress
import os

from flask import current_app

DEFAULT_LANGUAGE = 'en'
PASSWORD_ENCODING = 'utf8'
FULLTEXT_SEARCH_BIG_NUMBER=3000


def root_dir():
    return current_app.config['ROOT_DIR']


def machine_id():
    instance_ip = ipaddress.IPv4Address(os.environ.get('INSTANCE_PRIVATE_ID') or '127.0.0.1')
    _, digit2, digit3, _ = instance_ip.__str__().split('.')
    return int(digit2) << 8 | int(digit3)


def config_env():
    return os.environ.get('FLASK_ENV') or 'development'

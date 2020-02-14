import click
from airtable import Airtable
from flask.cli import AppGroup, with_appcontext
from models import db
from models.authorization.permission import Permission
from models.authorization.role import Role

import_cli = AppGroup('import', help='Import data from another source')
locales = ['en', 'fr', 'de', 'vi', 'nl']


@import_cli.command('roles', help='Import roles')
@click.option('-c', '--credentials', nargs=3, type=click.Tuple([str, str, str]),
              help='Airtable credential: BASE_KEY API_KEY TABLE_NAME', required=True)
@with_appcontext
def import_roles(credentials):
    source = _init_source(credentials)

    records = source.get_all()

    roles = {}
    permissions = {}

    for record in records:
        role_row = record['fields']
        role_name = role_row['Role']
        if role_name not in roles:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            roles[role_name] = new_role
        role = roles[role_name]

        permission_name = role_row['Permission']
        if permission_name not in permissions:
            new_permission = Permission(name=permission_name)
            db.session.add(new_permission)
            permissions[permission_name] = new_permission
        permission = permissions[permission_name]
        role.permissions.append(permission)

    db.session.commit()


def _init_source(credentials):
    base_key, api_key, table_name = credentials
    return Airtable(base_key, table_name, api_key)

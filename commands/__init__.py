from commands.import_ import import_cli


def init_app(app):
    app.cli.add_command(import_cli)

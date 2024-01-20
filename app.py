from importlib import import_module

from flask import Flask

from kanban.config import get_config


def load_extensions(app):
    for extension in get_config()['EXTENSIONS']:
        extension_module = import_module(extension)
        extension_module.init_app(app)


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = get_config()['SECRET_KEY']
    load_extensions(app)
    return app


app = create_app()

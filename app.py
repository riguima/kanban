from flask import Flask

from kanban import views
from kanban.config import get_config


def create_app():
    app = Flask(__name__)
    app.secret_key = get_config()['SECRET_KEY']
    views.init_app(app)
    return app


app = create_app()

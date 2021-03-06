from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_login import LoginManager

from config import configure_app

from app.data import db


migrate = Migrate(db)
login = LoginManager()
login.login_view = 'api.user.login'


def create_app(config="prod"):
    app = Flask(__name__)
    configure_app(app, config)

    cors = CORS(app, resources={
        r'/api/*': {
            'origins': app.config['ORIGINS']
        }
    })

    db.init_app(app)
    migrate.init_app(app)
    login.init_app(app)
    app.url_map.strict_slashes = False

    from app.data.models import models
    from app.api import controllers

    for prefix, bp in controllers:
        app.register_blueprint(bp, prefix=f"/api{prefix}")

    return app
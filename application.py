from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from config import config

from api.users.models import User, db

# Import Blueprints
from api.users.views import user_app


# db = SQLAlchemy()


def create_app(ENV):
    app = Flask(__name__)
    app.config.from_object(config.get(ENV))

    # setup_db
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_app)

    return app

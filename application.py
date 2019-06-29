from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from config import config
from api.utils.database import db, ma


# Import Blueprints
from api.users.views import user_app
from api.events.views import events_app
from api.programs.views import programs_app
from api.permissions.views import permissions_app
from api.roles.views import roles_app


# db = SQLAlchemy()


def create_app(ENV):
    app = Flask(__name__)
    app.config.from_object(config.get(ENV))

    # setup_db
    db.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    app.register_blueprint(user_app)
    app.register_blueprint(events_app)
    app.register_blueprint(programs_app)
    app.register_blueprint(permissions_app)
    app.register_blueprint(roles_app)
    


    return app

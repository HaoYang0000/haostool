import os
import sys
from flask import Flask
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(env=None):
    app = Flask(__name__, static_url_path='/static', )
    app._static_folder = os.path.join(
        os.path.dirname(__file__),
        'static'
    )

    # TODO: Implement vault style retrieval of username/password with service discovery for host/port`
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://haostool_admin:admin@localhost:3306/haostool_database?charset=utf8mb4"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    db.init_app(app)

    from app.views import index
    from app.views.accounting import main
    # from app.views import frequencies
    # from app.views import statuses
    # from app.views import types
    # from app.views import logs
    # from app.views import notifications
    # from app.views.rpc import get_unsent_notifications

    app.register_blueprint(index.app)
    app.register_blueprint(main.app)
    # app.register_blueprint(frequencies.app)
    # app.register_blueprint(statuses.app)
    # app.register_blueprint(types.app)
    # app.register_blueprint(logs.app)
    # app.register_blueprint(notifications.app)
    # app.register_blueprint(get_unsent_notifications.app)

    return app

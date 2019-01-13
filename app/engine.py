import os
import sys
from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_apispec import FlaskApiSpec
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from app.views.index import login_required
from werkzeug.utils import secure_filename
import config

db = SQLAlchemy()
login_manager = LoginManager()
socketIO = SocketIO()

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/static/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
CLOUDSQL_USER = "root"
CLOUDSQL_PASSWORD = "root"
CLOUDSQL_DATABASE = "haostool"
CLOUDSQL_CONNECTION_NAME = "haostool:us-central1:haostool"

def create_app():
    app = Flask(__name__, static_url_path='/static', )
    app._static_folder = os.path.join(
    	os.path.dirname(__file__),
    	'static'
    )

    if os.environ.get('GAE_ENV') == 'standard':
        LIVE_SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@localhost/{database}'
        '?unix_socket=/cloudsql/{connection_name}').format(
            user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
            database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)
        SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
    else:
        LOCAL_SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://{user}:{password}@35.226.253.240:3306/{database}').format(
            user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
            database=CLOUDSQL_DATABASE)
        SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key"
    ))
        
    db.init_app(app)
    login_manager.init_app(app)
    socketIO.init_app(app)

    from app.views import index
    from app.views.accounting import accounting
    from app.views.auth import auth
    from app.views.user import profile
    from app.views.socket_service import socket_service

    app.register_blueprint(index.app)
    app.register_blueprint(accounting.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(profile.app)
    app.register_blueprint(socket_service.app)

    app.register_error_handler(401, login_required)

    return app
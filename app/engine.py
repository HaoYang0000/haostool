import os
import sys
import platform
from flask import Flask, render_template, request, session
from flask_login import LoginManager
from flask_apispec import FlaskApiSpec
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
from werkzeug.utils import secure_filename
from config.config import get_database_uri, LANGUAGES
from flask_babel import Babel, gettext as _
import logging


handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

db = SQLAlchemy()
login_manager = LoginManager()
socketIO = SocketIO()
babel = Babel()
engine = create_engine(
    get_database_uri(),
    convert_unicode=True,
    pool_pre_ping=True,
    pool_recycle=300,
    isolation_level='READ UNCOMMITTED'
)

UPLOAD_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/static/uploads'
UPLOAD_ROOT = os.path.abspath(os.path.dirname(__file__)) + '/static'
USER_PROFILE_DIR = 'user_profile'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'zh')

def create_app():
    app = Flask(__name__, static_url_path='/static', )
    app._static_folder = os.path.join(
    	os.path.dirname(__file__),
    	'static'
    )

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = get_database_uri()
    app.config['BABEL_DEFAULT_LOCALE'] = 'zh_Hans_CN'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 60
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.secret_key="key"
    app.config.update(dict(
        WTF_CSRF_SECRET_KEY="a csrf secret key"
    ))
        
    
    db.init_app(app)
    login_manager.init_app(app)
    socketIO.init_app(app)
    babel.init_app(app)
    app.logger.addHandler(handler)



    from app.views import index
    from app.views.accounting import accounting
    from app.views.auth import auth
    from app.views.user import profile
    from app.views.socket_service import socket_service
    from app.views.games import games
    from app.views.aws import aws
    from app.views.videos import videos
    # from app.views.streaming import streaming
    from app.views.shadow_url import shadow_url
    from app.views.blog import blog
    from app.views.index import login_required

    app.register_blueprint(index.app)
    app.register_blueprint(accounting.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(profile.app)
    app.register_blueprint(games.app)
    app.register_blueprint(socket_service.app)
    app.register_blueprint(aws.app)
    app.register_blueprint(videos.app)
    # app.register_blueprint(streaming.app)
    app.register_blueprint(shadow_url.app)
    app.register_blueprint(blog.app)


    app.register_error_handler(401, login_required)

    return app

@contextmanager
def session_scope():
    """
    Provide a transactional scope around a series of operations.
    This is the preferred way to get a session. It ensures a commit,
    optional rollback, and close
    """
    current_session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
    )
    try:
        yield current_session
    except Exception as exception:
        raise exception
    finally:
        current_session.remove()
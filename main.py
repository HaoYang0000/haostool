import os
import sys
from flask import Flask, render_template, request
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()

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

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        
    db.init_app(app)

    from views import index
    from views.accounting import accounting

    app.register_blueprint(index.app)
    app.register_blueprint(accounting.app)

    return app

app = create_app()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app = create_app()
    app.run(host='127.0.0.1', port=8080, debug=True)
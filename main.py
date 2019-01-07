import os
import sys
from flask import Flask, render_template, request
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__, static_url_path='/static', )
app._static_folder = os.path.join(
	os.path.dirname(__file__),
	'static'
)

LOCAL_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@35.226.253.240:3306/{database}').format(
        user="root", password="root",
        database="haostool")

# When running on App Engine a unix socket is used to connect to the cloudsql
# instance.
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user="root", password="root",
        database="haostool", connection_name="haostool:us-central1:haostool")

if os.environ.get('GAE_INSTANCE'):
    app.config['SQLALCHEMY_DATABASE_URI'] = LIVE_SQLALCHEMY_DATABASE_URI
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_SQLALCHEMY_DATABASE_URI

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
db.init_app(app)

from views import index
from views.accounting import main


app.register_blueprint(index.app)
app.register_blueprint(main.app)


@app.route('/')
def index():
    return render_template('index.html')
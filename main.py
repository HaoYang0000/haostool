import os
import sys
from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_apispec import FlaskApiSpec
from flask_sqlalchemy import SQLAlchemy
import config
from app.engine import create_app, socketIO
from flask_socketio import SocketIO

app = create_app()

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    # app.run(host='127.0.0.1', port=8080, debug=True)
    socketIO.run(app, host='127.0.0.1', debug=True)
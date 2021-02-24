import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, send_from_directory
from flask_api import status
from flask import send_from_directory


UPLOAD_FOLDER = '/backend/uploads/'
app = Blueprint('index', __name__)
logger = logging.getLogger(__name__)

# controller = Controller(current_user=current_user)


@app.route('/health', methods=['GET', 'POST'])
def health():
    return 'OK', status.HTTP_201_CREATED


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

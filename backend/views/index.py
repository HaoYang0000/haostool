import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, send_from_directory
from flask_api import status
from flask_login import current_user, login_user, logout_user
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
    logger.error(request.headers.get('Accept-Language', ''))
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        all_service = controller.get_all_service()
        return render_template('index.html', current_user=current_user, all_service=all_service)

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(401)
def login_required(e):
    # note that we set the 404 status explicitly
    return redirect('/auth/login'), 401


@app.errorhandler(Exception)
def exception_handler(error):
    return "!!!!" + repr(error)

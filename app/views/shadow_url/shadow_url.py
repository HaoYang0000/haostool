import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_socketio import SocketIO, send, emit
from app.engine import db, socketIO
from flask_login import login_required

import uuid

app = Blueprint(
    'shadow_url',
    __name__,
    url_prefix='/shadow_url'
)
logger = logging.getLogger(__name__)


@app.route('/show_secret_service', methods=['POST'])
@login_required
def shadow_url():
    data = request.form['token']

    # verify token
    url = url_for('index.special')

    generated_tag = f'<a class="nav-button right-align" href="{url}">特殊内容</a>'
    logger.error(generated_tag)
    return jsonify(generated_tag)

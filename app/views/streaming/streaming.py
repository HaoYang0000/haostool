from importlib import import_module
import json
import logging
import os
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, Response
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_cors import cross_origin
from app.engine import UPLOAD_ROOT

app = Blueprint('streaming', __name__)
logger = logging.getLogger(__name__)


@app.route('/streaming', methods=['GET', 'POST'])
@cross_origin()
def streaming():
    is_streaming = os.path.exists(f"{UPLOAD_ROOT}/live/index.m3u8")
    return render_template('streaming/streaming.html', is_streaming=is_streaming)

import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response
from flask_api import status
from flask_login import current_user, login_user, logout_user


app = Blueprint('videos', __name__)
logger = logging.getLogger(__name__)


@app.route('/videos', methods=['GET', 'POST'])
def videos():
    return render_template('videos/videos.html')

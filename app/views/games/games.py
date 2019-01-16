import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_socketio import SocketIO, emit
from app.engine import db, socketIO 

app = Blueprint('games', __name__)
logger = logging.getLogger(__name__)

@app.route('/felix')
def felix():
    return render_template('games/felix.html')

@app.route('/super_mario')
def super_mario():
    return render_template('games/super_mario.html')
import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_socketio import SocketIO, emit
from app.engine import db, socketIO 

app = Blueprint(
    'socket_service',
    __name__,
    url_prefix='/socket_service'
)
logger = logging.getLogger(__name__)

@app.route('/')
def sessions():
    return render_template('socket_service/socket_service.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketIO.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: '+ str(json))
    socketIO.emit('my response', json, callback=messageReceived)
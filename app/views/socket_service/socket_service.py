import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_socketio import SocketIO, send, emit
from app.engine import db, socketIO
from flask_login import login_required
from app.models.socket_service.game_room import GameRoomModel
from app.forms.socket_service.create_game_room import CreateGameRoomForm
import uuid
from app.engine import session_scope

app = Blueprint(
    'socket_service',
    __name__,
    url_prefix='/socket_service'
)
logger = logging.getLogger(__name__)


@app.route('/')
def view_rooms():
    with session_scope() as session:
        form = CreateGameRoomForm()
        game_rooms = session.query(GameRoomModel).all()
        return render_template('socket_service/socket_service.html', form=form, rooms=game_rooms)


@app.route('/enter_room/<string:room_uuid>', methods=['GET'])
def enter_room(room_uuid):
    return render_template('socket_service/game_room.html', room_id=room_uuid)


@app.route('/create_room', methods=['POST'])
def create_room():
    with session_scope() as session:
        form = CreateGameRoomForm()
        if form.validate_on_submit():
            game_room = GameRoomModel(
                name=form.name.data,
                uuid=uuid.uuid4().hex,
                expire_at=form.expire_at.data
            )
            session.add(game_room)
            session.commit()

        return redirect(url_for('socket_service.view_rooms'))


def messageReceived(methods=['GET', 'POST']):
    print('kglb')


@socketIO.on('game_room')
# @login_required
def handle_my_custom_event(message: dict, methods=['GET', 'POST']):
    # mydict = {k: v.encode('raw_unicode_escape').decode('utf8') for k, v in message.items()}
    print('received my event: ' + str(message))
    socketIO.emit('responses', message, callback=messageReceived)
# socketIO.emit('responses', {'user_name': '柯哥流弊', 'message': '威哥逗比'})

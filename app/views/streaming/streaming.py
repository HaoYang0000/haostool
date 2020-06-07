from importlib import import_module
import json
import logging
import os
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, Response
from flask_api import status
from flask_login import current_user, login_user, logout_user
from flask_cors import cross_origin
# from app.services.streaming.streaming import Camera

app = Blueprint('streaming', __name__)
logger = logging.getLogger(__name__)

# def gen(camera):
#     """
#     流媒体发生器
#     """
#     while True:
#         frame = camera.get_frame()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed', methods=['GET', 'POST'])
# def video_feed():
#     return Response(gen(Camera()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/streaming', methods=['GET', 'POST'])
@cross_origin()
def streaming():
    return render_template('streaming/streaming.html')

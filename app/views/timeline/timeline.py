import json
import logging
import os
import subprocess
import time
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
import uuid
from app.services.timeline.timeline_service import TimelineService
from app.engine import session_scope
from app.utils import admin_required

app = Blueprint(
    'timeline',
    __name__,
    url_prefix='/timeline')
logger = logging.getLogger(__name__)

timeline_service = TimelineService()

@app.route('/', methods=['POST'])
@admin_required
def video_comment():
    pass
    # comment_service = CommentService()
    # form = VideoCommentForm()
    # if form.is_submitted():
    #     new_comment = comment_service.create(
    #         user_id=None if not current_user.is_authenticated else current_user.id,
    #         unknown_user_name=form.unknown_user_name.data,
    #         content=form.content.data,
    #         category='video',
    #         video_uuid=form.video_uuid.data
    #     )
    #     comment = new_comment.serialize
    #     if current_user.is_authenticated:
    #         user = UserService().get_by_id(current_user.id).serialize
    #         comment['user'] = {
    #             'avatar': user.get('avatar')
    #         }
    #     if new_comment:
    #         return comment, 200
    # return 'err', 400
@app.route('/', methods=['GET'])
def timelines():
    return render_template('timeline/timeline.html')

@app.route('/get_timelines', methods=['GET'])
def get_timelines():
    html = ""
    timelines = timeline_service.get_all()
    for timeline in timelines:
        html+= f"<li>{timeline.message}  --  {timeline.created_at}</li>"
    return html

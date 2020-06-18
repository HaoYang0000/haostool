import json
import logging
import os
import subprocess
import time
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
import uuid
from app.services.comment.comment_service import CommentService
from app.forms.comment.video_comment import VideoCommentForm
from app.services.user.user_service import UserService
from app.engine import session_scope
from app.utils import admin_required

app = Blueprint(
    'comment',
    __name__,
    url_prefix='/comment')
logger = logging.getLogger(__name__)


@app.route('/video/post', methods=['POST'])
def video_comment():
    comment_service = CommentService()
    form = VideoCommentForm()
    if form.is_submitted():
        new_comment = comment_service.create(
            user_id=None if not current_user.is_authenticated else current_user.id,
            unknown_user_name=form.unknown_user_name.data,
            content=form.content.data,
            category='video',
            video_uuid=form.video_uuid.data
        )
        comment = new_comment.serialize
        if current_user.is_authenticated:
            user = UserService().get_by_id(current_user.id).serialize
            comment['user'] = {
                'avatar': user.get('avatar')
            }
        if new_comment:
            return comment, 200
    return 'err', 400

@app.route('/', methods=['GET'])
def comment_page():
    comment_service = CommentService()
    comments = comment_service.get_all_feedback_comment()
    return render_template('comment.html', comments=comments)

@app.route('/feedback/post', methods=['POST'])
def feedback_comment():
    comment_service = CommentService()
    comment_service.create(
        user_id=None if not current_user.is_authenticated else current_user.id,
        unknown_user_name=request.form['unknown_user_name'],
        content=request.form['content'],
        contact_email=request.form['contact_email'],
        category='feedback'
    )
    return redirect(url_for('comment.comment_page'))

@app.route('/deactivate_comment', methods=['POST'])
@admin_required
def delete_comment():
    comment_service = CommentService()
    result = comment_service.deactive_comment(id=request.form['comment_id'])
    if result:
        return 'success', 200
    return 'err', 400
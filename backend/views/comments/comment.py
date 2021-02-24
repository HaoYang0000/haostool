import json
import logging
import os
import subprocess
import time
import flask_praetorian
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
import uuid
from backend.services.comments.comment_service import CommentService
from backend.services.users.user_service import UserService
from backend.engine import session_scope


app = Blueprint(
    'comments',
    __name__,
    url_prefix='/comments')
logger = logging.getLogger(__name__)
comment_service = CommentService()

# @app.route('/video', methods=['POST'])
# def video_comment():
#     comment_service = CommentService()
#     form = CommentForm()
#     if form.is_submitted():
#         new_comment = comment_service.create(
#             user_id=None if not current_user.is_authenticated else current_user.id,
#             unknown_user_name=form.unknown_user_name.data,
#             content=form.content.data,
#             category='video',
#             video_uuid=form.video_uuid.data
#         )
#         comment = new_comment.serialize
#         if current_user.is_authenticated:
#             user = UserService().get_by_id(current_user.id).serialize
#             comment['user'] = {
#                 'avatar': user.get('avatar')
#             }
#         if new_comment:
#             return comment, 200
#     return 'err', 400


@app.route('/feedback', methods=['GET'])
def get_feedback_comment():
    comments = comment_service.get_all_feedback_comment()
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/video', methods=['GET'])
def get_video_comment():
    comments = comment_service.get_all_video_comment()
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/video/<string:uuid>', methods=['GET'])
def get_video_comment_for_uuid(uuid):
    comments = comment_service.get_reply_for_video_uuid(video_uuid=uuid)
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/blog', methods=['GET'])
def get_blog_comment():
    comments = comment_service.get_all_blog_comment()
    return jsonify([comment.serialize for comment in comments]), 200


@app.route('/blog/<string:uuid>', methods=['GET'])
def get_blog_comment_for_uuid(uuid):
    comments = comment_service.get_reply_for_blog_uuid(blog_uuid=uuid)
    return jsonify([comment.serialize for comment in comments]), 200


# @app.route('/blog', methods=['POST'])
# def blog_comment():
#     comment_service = CommentService()
#     comment_service.create(
#         user_id=None if not current_user.is_authenticated else current_user.id,
#         unknown_user_name=request.form['unknown_user_name'],
#         content=request.form['content'],
#         contact_email=request.form['contact_email'],
#         category='blog',
#         blog_uuid=request.form['blog_uuid']
#     )
#     return redirect(f"/blog/view/{request.form['blog_uuid']}")

@app.route('/post-new', methods=['POST'])
def post_new_comment():
    comment_service.create(
        user_id=request.form['user_id'] if 'user_id' in request.form else None,
        unknown_user_name=request.form['name'],
        content=request.form['content'],
        contact_email=request.form['email'] if 'email' in request.form else None,
        category=request.form['category'],
        blog_uuid=request.form['blog_uuid'] if 'blog_uuid' in request.form else None,
        video_uuid=request.form['video_uuid'] if 'video_uuid' in request.form else None,
    )
    return jsonify('success'), 200


@app.route('/deactivate-comment', methods=['POST'])
@flask_praetorian.roles_required(*['root'])
def delete_comment():
    req = request.get_json(force=True)
    result = comment_service.deactive_comment(id=req.get('comment_id'))
    if result:
        return jsonify('success'), 200
    return jsonify('err'), 400

import json
import logging
import os
import math
import subprocess
import flask_praetorian
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
from backend.services.videos.video_service import VideoService
from werkzeug.utils import secure_filename
from backend.engine import UPLOAD_ROOT, DEFAULT_PAGE_LIMIT
import uuid
# from app.services.comment.comment_service import CommentService
from pypinyin import pinyin, lazy_pinyin

app = Blueprint('videos', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)
VIDEOS_FOLDER = 'videos'
video_service = VideoService()


@app.route('/videos', methods=['GET'])
def videos():
    video_service = VideoService()
    videos = video_service.get_videos(
        category=request.args.get('category'),
        order=request.args.get('order'),
        sort_by=request.args.get('sortBy'),
        page=int(request.args.get('page')),
    )

    return jsonify({
        'videos': [video.serialize for video in videos],
        'count': math.ceil(video_service.get_total_page_len(category=request.args.get('category')) / DEFAULT_PAGE_LIMIT)
    }), 200


@app.route('/videos/get-all', methods=['GET'])
def all_videos():
    video_service = VideoService()
    videos = video_service.get_all_videos_created_desc()
    return jsonify([video.serialize for video in videos]), 200


@app.route('/videos/<string:uuid>', methods=['GET'])
def view_video(uuid):
    video_service = VideoService()
    video = video_service.get_video_by_uuid(uuid=uuid)
    # comment_service = CommentService()

    if video:
        video_service._view_increase(video)
        #comments = comment_service.get_reply_for_video_uuid(video_uuid=uuid)
        return video.serialize, 200
    return jsonify("No video found"), 404


@app.route('/videos/like/<string:uuid>', methods=['POST'])
def like_video(uuid):
    video_service = VideoService()
    video = video_service.get_video_by_uuid(uuid=uuid)
    current_num = video.liked_number
    if video:
        video_service._like_increase(video)
        return jsonify(current_num), 200
    else:
        return jsonify("No video found"), 400


@app.route('/videos/delete', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_video():
    req = request.get_json(force=True)
    video = video_service.get_by_id(id=req.get('video_id'))
    os.remove(f"{UPLOAD_ROOT}/{video.path}")
    os.remove(f"{UPLOAD_ROOT}/{video.thumb_nail}")
    result = video_service.delete_by_id(id=req.get('video_id'))
    if result:
        return jsonify("success"), 200
    return jsonify("err"), 400


@app.route('/videos/increase_star', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def video_increase_star():
    req = request.get_json(force=True)
    result = video_service.increse_star(id=req.get('video_id'))
    if result:
        return jsonify(f"Current star: {result}"), 200
    return jsonify("err"), 400


@app.route('/videos/decrease_star', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def video_decrease_star():
    req = request.get_json(force=True)
    result = video_service.decrease_star(id=req.get('video_id'))
    if result:
        return jsonify(f"Current star: {result}"), 200
    return jsonify("err"), 400


@app.route('/videos/upload', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def upload_video():
    # check if the post request has the file part
    if 'file' not in request.files:
        logger.error('No file part')
        return jsonify("err"), 400

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        logger.error('No selected file')
        return jsonify("err"), 400

    uuid_val = uuid.uuid4().hex
    # save file
    filename = secure_filename(str(lazy_pinyin(file.filename)))
    file.save(f"{UPLOAD_ROOT}/{VIDEOS_FOLDER}/{filename}")

    video_input_path = f"{UPLOAD_ROOT}/{VIDEOS_FOLDER}/{filename}"
    img_output_path = f"{UPLOAD_ROOT}/{VIDEOS_FOLDER}/{uuid_val}.gif"

    # Generate thumb nail
    subprocess.call(['ffmpeg', '-t', '3', '-r', '10', '-i',
                     video_input_path, '-ss', '00:00:00.000',  img_output_path])

    # Create model
    new_video = VideoService().create(
        title=request.form['title'],
        category=request.form['category'],
        path=f"{VIDEOS_FOLDER}/{filename}",
        uuid=uuid_val,
        thumb_nail=f"{VIDEOS_FOLDER}/{uuid_val}.gif"
    )

    logger.info('File upload successful')
    return jsonify("success"), 200

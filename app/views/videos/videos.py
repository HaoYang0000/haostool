import json
import logging
import os
import subprocess
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
from flask_login import current_user, login_user, logout_user
from app.services.videos.video_service import VideoService
from werkzeug.utils import secure_filename
from app.engine import UPLOAD_ROOT
import uuid
from app.forms.comment.video_comment import VideoCommentForm
from app.services.comment.comment_service import CommentService
from pypinyin import pinyin, lazy_pinyin

app = Blueprint('videos', __name__)
logger = logging.getLogger(__name__)
VIDEOS_FOLDER = 'videos'

@app.route('/videos', methods=['GET', 'POST'])
def videos():
    video_service = VideoService()
    videos = video_service.get_all()
    return render_template('videos/all_videos.html', videos=videos)

@app.route('/videos/<string:uuid>', methods=['GET', 'POST'])
def view_video(uuid):
    video_service = VideoService()
    video = video_service.get_video_by_uuid(uuid=uuid)
    video_form = VideoCommentForm() 
    comment_service = CommentService()

    if video:
        video_service._view_increase(video)
        src = f"/static/{video.path}"
        comments = comment_service.get_reply_for_video_uuid(video_uuid=uuid)
        return render_template('videos/view_video.html', 
                                src=src, 
                                viewed_num=video.viewed_number, 
                                liked_num=video.liked_number, 
                                uuid=video.uuid,
                                video_form=video_form,
                                comments=comments
                            )
    else:
        flash('No video found')
        return redirect(url_for('videos.videos'))

@app.route('/videos/like/<string:uuid>', methods=['POST'])
def like_video(uuid):
    video_service = VideoService()
    video = video_service.get_video_by_uuid(uuid=uuid)
    current_num = video.liked_number
    if video:
        video_service._like_increase(video)
        return str(current_num + 1)
    else:
        return "No video found"

@app.route('/videos/upload', methods=['GET'])
def upload_video_page():
    videos = VideoService().get_all()
    return render_template('videos/upload.html', videos=videos)

@app.route('/videos/upload', methods=['POST'])
def upload_video():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('videos.upload_video_page'))

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('videos.upload_video_page'))

    uuid_val = uuid.uuid4().hex
    # save file
    filename = secure_filename(str(lazy_pinyin(file.filename)))
    file.save(f"{UPLOAD_ROOT}/{VIDEOS_FOLDER}/{filename}")

    video_input_path = f"{UPLOAD_ROOT}/{VIDEOS_FOLDER}/{filename}"
    img_output_path = f"{UPLOAD_ROOT}/{VIDEOS_FOLDER}/{uuid_val}.gif"

    # Generate thumb nail
    subprocess.call(['ffmpeg', '-t', '3', '-r', '10', '-i', video_input_path, '-ss', '00:00:00.000',  img_output_path])

    # Create model
    new_video = VideoService().create(
        title=request.form['title'],
        category=request.form['category'],
        path=f"{VIDEOS_FOLDER}/{filename}",
        uuid=uuid_val,
        thumb_nail=f"{VIDEOS_FOLDER}/{uuid_val}.gif"
    )
    
    flash('File upload successful')
    return "success"
import json
import logging

from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request
from flask_api import status
from flask_login import current_user, login_user, logout_user, login_required
from app.services.blog.blog_service import BlogService
from app.forms.blog.create_post_form import CreateBlogPostForm
from app.engine import session_scope
from werkzeug.utils import secure_filename
from app.utils import allowed_file
from app.engine import UPLOAD_ROOT, BLOG_IMAGE_DIR

import uuid
import pickle

app = Blueprint(
    'blog',
    __name__,
    url_prefix='/blog'
)
logger = logging.getLogger(__name__)

blog_service = BlogService()
SINGLE_QUOTE = '__SINGLE_QUOTE__'

@app.route('/', methods=['GET'])
def blogs():
    posts = BlogService().get_all()
    return render_template('blog/blog.html', posts=posts)

@app.route('/view/<string:uuid>', methods=['GET'])
def view_blogs(uuid):
    post = BlogService().get_posts_by_uuid(uuid=uuid)
    content = post.content
    logger.error(content)
    return render_template('blog/view_blog.html', post=post, content=content)

@app.route('/edit/<string:uuid>', methods=['GET'])
@login_required
def edit_post(uuid):
    post = BlogService().get_posts_by_uuid(uuid=uuid)
    content = post.content
    form = CreateBlogPostForm()
    logger.error(content)
    return render_template('blog/edit_post.html', post=post, form=form, content=content)

@app.route('/edit/<string:uuid>', methods=['POST'])
@login_required
def update_post(uuid):
    form = CreateBlogPostForm()
    if form.is_submitted():
        content=form.content.data
        post = BlogService().update_by_uuid(
            uuid=uuid,
            title=form.title.data,
            content=content
        )
        if post:
            return "success", 200
    return "err", 400

@app.route('/create_post', methods=['GET'])
@login_required
def create_post_main():
    form = CreateBlogPostForm()
    return render_template('blog/create_post.html', form=form)

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    form = CreateBlogPostForm()
    if form.is_submitted():
        new_blog = BlogService().create(
            title=form.title.data,
            content=form.content.data,
            uuid=uuid.uuid4().hex
        )
        logger.error(new_blog)
        if new_blog:
            return 'success', 200
    return 'err',400


@app.route('/image_upload', methods=['POST'])
def blog_upload_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No file name", 400
    if not allowed_file(file.filename):
        flash('File format not allowed')
        return redirect(url_for('user.profile'))

    filename = secure_filename(file.filename)
    file.save(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}/{filename}")
    return {"link": url_for('static', filename=f'{BLOG_IMAGE_DIR}/{filename}')}, 200

@app.route('/video_upload', methods=['POST'])
def video_upload_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No file name", 400
    if not allowed_file(file.filename):
        flash('File format not allowed')
        return redirect(url_for('user.profile'))

    filename = secure_filename(file.filename)
    file.save(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}/{filename}")
    return {"link": url_for('static', filename=f'{BLOG_IMAGE_DIR}/{filename}')}, 200

@app.route('/file_upload', methods=['POST'])
def file_upload_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return "No file name", 400
    if not allowed_file(file.filename):
        flash('File format not allowed')
        return redirect(url_for('user.profile'))

    filename = secure_filename(file.filename)
    file.save(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}/{filename}")
    return {"link": url_for('static', filename=f'{BLOG_IMAGE_DIR}/{filename}')}, 200

def __format_str(str):
    str = str.replace('\r','\\r')
    str = str.replace('\n','\\n')
    # str = str.replace('\t','\\t')
    # str = str.replace('"','&quot;')
    # str = str.replace("'", "\\'")

    str = str.replace("'", "\\'")
    return str

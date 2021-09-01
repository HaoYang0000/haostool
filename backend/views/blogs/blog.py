import json
import os
import math
import uuid
import flask_praetorian
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request
from flask_api import status
from flask_login import current_user, login_user, logout_user, login_required
from backend.services.blogs.blog_service import BlogService
from backend.engine import session_scope, DEFAULT_PAGE_LIMIT
from werkzeug.utils import secure_filename
from backend.utils.utils import allowed_profile_img_format
from backend.engine import UPLOAD_ROOT, BLOG_IMAGE_DIR
from pypinyin import pinyin, lazy_pinyin
from backend.logs.logger import logger


app = Blueprint(
    'blogs',
    __name__,
    url_prefix='/api/blogs'
)

blog_service = BlogService()
# comment_service = CommentService()
SINGLE_QUOTE = '__SINGLE_QUOTE__'


@app.route('/', methods=['GET'])
def blogs():
    posts = blog_service.get_blogs(
        order=request.args.get('order'),
        sort_by=request.args.get('sortBy'),
        page=int(request.args.get('page')),
    )
    return jsonify({
        'blogs': [post.serialize for post in posts],
        'count': math.ceil(len(blog_service.get_all_published_blogs()) / DEFAULT_PAGE_LIMIT)
    }), 200


@ app.route('/get-all', methods=['GET'])
def all_blogs():
    blogs = blog_service.get_all_published_blogs()
    return jsonify([blog.serialize for blog in blogs]), 200


@ app.route('/fetch/<string:uuid>', methods=['GET'])
def view_blogs(uuid):
    post = blog_service.get_posts_by_uuid(uuid=uuid)
    # comment_form = CommentForm()
    if post:
        blog_service.view_increase(post)
        # comments = comment_service.get_reply_for_blog_uuid(blog_uuid=uuid)
        return jsonify(post.serialize), 200
    return jsonify("No blog found"), 404


# @app.route('/edit/<string:uuid>', methods=['GET'])
# @login_required
# def edit_post(uuid):
#     post = BlogService().get_posts_by_uuid(uuid=uuid)
#     content = post.content
#     form = CreateBlogPostForm()
#     return render_template('blog/edit_post.html', post=post, form=form, content=content)


@ app.route('/edit/<string:uuid>', methods=['POST'])
@ flask_praetorian.roles_accepted(*['root', 'admin'])
def update_post(uuid):
    cover_img_path = None
    if 'file' in request.files:
        file = request.files['file']
        filename = secure_filename(str(lazy_pinyin(file.filename)))
        cover_img_path = f"{BLOG_IMAGE_DIR}/{filename}"
        file.save(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}/{filename}")

    blog_service.update_by_uuid(
        uuid=uuid,
        title=request.form['title'],
        content=request.form['content'],
        blog_intro=request.form['intro'],
        cover_img=cover_img_path
    )
    return jsonify('Update success'), 200


# @app.route('/like/<string:uuid>', methods=['POST'])
# def like_blog(uuid):
#     blog = blog_service.get_posts_by_uuid(uuid=uuid)
#     current_num = blog.liked_number
#     if blog:
#         blog_service.like_increase(blog)
#         return str(current_num + 1)
#     else:
#         return "No blog found"


# @app.route('/delete', methods=['DELETE'])
# @admin_required
# def delete_post():
#     result = blog_service.delete_by_id(id=request.form['post_id'])
#     if result:
#         return "success", 200
#     return "err", 400


@ app.route('/publish', methods=['POST'])
@ flask_praetorian.roles_accepted(*['root', 'admin'])
def publish_post():
    req = request.get_json(force=True)
    result = blog_service.publish_blog(blog_id=req.get('blog_id'))
    if result:
        return jsonify("success"), 200
    return jsonify("err"), 400


@ app.route('/unpublish', methods=['POST'])
@ flask_praetorian.roles_accepted(*['root', 'admin'])
def unpublish_post():
    req = request.get_json(force=True)
    result = blog_service.unpublish_blog(blog_id=req.get('blog_id'))
    if result:
        return jsonify("success"), 200
    return jsonify("err"), 400


# @app.route('/create_post', methods=['GET'])
# @admin_required
# def create_post_main():
#     form = CreateBlogPostForm()
#     return render_template('blog/create_post.html', form=form)


@ app.route('/create-post', methods=['POST'])
@ flask_praetorian.roles_accepted(*['root', 'admin'])
def create_post():
    if 'file' not in request.files:
        logger.error('No file part')
        return jsonify("No file part"), 401

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        logger.error('No selected file')
        return jsonify("No selected file"), 402

    filename = secure_filename(str(lazy_pinyin(file.filename)))
    file.save(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}/{filename}")
    cover_img_path = f"{BLOG_IMAGE_DIR}/{filename}"
    new_blog = blog_service.create(
        title=request.form['title'],
        content=request.form['content'],
        uuid=uuid.uuid4().hex,
        blog_intro=request.form['intro'],
        cover_img=cover_img_path,
        liked_number=0,
        viewed_number=0
    )
    return jsonify('Create blog success'), 200


@ app.route('/file_upload', methods=['POST'])
def file_upload_image():
    # check if the post request has the file part
    if 'file' not in request.files:
        return jsonify("No file part"), 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify("No file name"), 400
    if not allowed_profile_img_format(file.filename):
        return jsonify('File format not allowed'), 400

    if not os.path.exists(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}"):
        logger.warning(
            f"folder: {UPLOAD_ROOT}/{BLOG_IMAGE_DIR} does not exist. Creating folder")
        os.makedirs(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}")

    filename = secure_filename(file.filename)
    file.save(f"{UPLOAD_ROOT}/{BLOG_IMAGE_DIR}/{filename}")
    return {"link": url_for('static', filename=f'{BLOG_IMAGE_DIR}/{filename}')}, 200


def __format_str(str):
    str = str.replace('\r', '\\r')
    str = str.replace('\n', '\\n')
    # str = str.replace('\t','\\t')
    # str = str.replace('"','&quot;')
    # str = str.replace("'", "\\'")

    str = str.replace("'", "\\'")
    return str

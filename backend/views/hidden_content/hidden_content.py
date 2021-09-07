import json
import uuid
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response
from flask_api import status
from flask_login import current_user, login_user, logout_user
from backend.services.blogs.blog_service import BlogService
from flask import send_from_directory
from collections import namedtuple
import flask_praetorian
from backend.logs.logger import logger

app = Blueprint('hidden_content', __name__, url_prefix='/api/hidden-content')
blog_service = BlogService()


@app.route('/config/update', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def hidden_content_config_update():
    result = blog_service.update_hidden_content_config(
        id=request.form['id'],
        name=request.form['name'],
        uuid=request.form['uuid']
    )
    return jsonify(result), 200


@app.route('/categories', methods=['GET'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def get_all_hidden_content_categories():
    categories = blog_service.get_all_hidden_content_categories()
    return jsonify([category.serialize for category in categories]), 200


@app.route('/categories', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def create_hidden_content_category():
    uuid_val = uuid.uuid4().hex
    blog_service.create_hidden_content_category(
        name=request.form['name'],
        uuid=uuid_val
    )
    return jsonify('Create category success'), 200


@app.route('/categories', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_hidden_content_category():
    blog_service.delete_hidden_content_category_by_id(id=request.form['id'])
    return jsonify('Delete category success'), 200


@app.route('/content/<string:uuid>', methods=['GET'])
def get_hidden_content_by_uuid(uuid):
    blogs = blog_service.get_hidden_blogs_by_hidden_bridge_uuid(uuid=uuid)
    return jsonify(blogs), 200


@app.route('/blogs', methods=['GET'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def get_hidden_blogs():
    blogs = blog_service.get_all_hidden_blogs()
    return jsonify([blog.serialize for blog in blogs]), 200


@app.route('/link-blogs', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def link_hidden_category_with_blogs():
    logger.info(request.form['blog_id'])
    logger.info(request.form['hidden_content_id'])
    result = blog_service.link_hidden_category_with_blog(
        blog_id=request.form['blog_id'],
        hidden_content_id=request.form['hidden_content_id']
    )
    return jsonify(result), 200


@app.route('/link-blogs', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def unlink_hidden_category_with_blogs():
    result = blog_service.unlink_hidden_category_with_blog(
        blog_id=request.form['blog_id'],
        hidden_content_id=request.form['hidden_content_id']
    )
    return jsonify(result), 200

# @app.route('/delete', methods=['DELETE'])
# @flask_praetorian.roles_accepted(*['root', 'admin'])
# def delete_label():
#     label_service.delete_by_id(id=request.form['id'])
#     return jsonify('Delete label success'), 200


# @app.route('/create/blog-label', methods=['POST'])
# @flask_praetorian.roles_accepted(*['root', 'admin'])
# def create_blog_label():
#     result = label_service.create_label_for_blog(
#         label_id=request.form['label_id'], blog_id=request.form['blog_id'])
#     return jsonify(result), 200


# @app.route('/delete/blog-label', methods=['DELETE'])
# @flask_praetorian.roles_accepted(*['root', 'admin'])
# def delete_blog_label():
#     print(request.form)
#     result = label_service.delete_label_for_blog(
#         label_id=request.form['label_id'], blog_id=request.form['blog_id'])
#     return jsonify(result), 200


# @app.route('/create/video-label', methods=['POST'])
# @flask_praetorian.roles_accepted(*['root', 'admin'])
# def create_video_label():
#     result = label_service.create_label_for_video(
#         label_id=request.form['label_id'], video_id=request.form['video_id'])
#     return jsonify(result), 200


# @app.route('/delete/video-label', methods=['DELETE'])
# @flask_praetorian.roles_accepted(*['root', 'admin'])
# def delete_video_label():
#     print(request.form)
#     result = label_service.delete_label_for_video(
#         label_id=request.form['label_id'], video_id=request.form['video_id'])
#     return jsonify(result), 200

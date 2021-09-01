import json
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response
from flask_api import status
from flask_login import current_user, login_user, logout_user
from backend.services.labels.label_service import LabelService
from flask import send_from_directory
from collections import namedtuple
import flask_praetorian
from backend.logs.logger import logger

app = Blueprint('labels', __name__, url_prefix='/api/labels')
label_service = LabelService()


@app.route('', methods=['GET'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def get_labels():
    labels = label_service.get_all()
    return jsonify([label.serialize for label in labels]), 200


@app.route('/create', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def create_label():
    label_service.create(
        name=request.form['name']
    )
    return jsonify('Create label success'), 200


@app.route('/delete', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_label():
    label_service.delete_by_id(id=request.form['id'])
    return jsonify('Delete label success'), 200


@app.route('/create/blog-label', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def create_blog_label():
    result = label_service.create_label_for_blog(
        label_id=request.form['label_id'], blog_id=request.form['blog_id'])
    return jsonify(result), 200


@app.route('/delete/blog-label', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_blog_label():
    print(request.form)
    result = label_service.delete_label_for_blog(
        label_id=request.form['label_id'], blog_id=request.form['blog_id'])
    return jsonify(result), 200


@app.route('/create/video-label', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def create_video_label():
    result = label_service.create_label_for_video(
        label_id=request.form['label_id'], video_id=request.form['video_id'])
    return jsonify(result), 200


@app.route('/delete/video-label', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_video_label():
    print(request.form)
    result = label_service.delete_label_for_video(
        label_id=request.form['label_id'], video_id=request.form['video_id'])
    return jsonify(result), 200

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

@app.route('/', methods=['GET'])
def timelines():
    timelines = timeline_service.get_all()
    return render_template('timeline/timeline.html', timelines=timelines)

@app.route('/add', methods=['POST'])
@admin_required
def add_timeline():
    timeline_service.create(
        title=request.form['timeline_title'],
        content=request.form['timeline_content']
    )
    return redirect(url_for('timeline.timelines'))

@app.route('/disable', methods=['POST'])
@admin_required
def disable_timeline():
    result = timeline_service.deactive_timeline(id=request.form['timeline_id'])
    if result:
        return 'success', 200
    return 'err', 400

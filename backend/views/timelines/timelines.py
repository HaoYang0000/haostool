import json
import os
import subprocess
import time
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, make_response, url_for
from flask_api import status
import flask_praetorian
import uuid
from backend.services.timelines.timeline_service import TimelineService
from backend.engine import session_scope
from backend.logs.logger import logger
app = Blueprint(
    'timelines',
    __name__,
    url_prefix='/api/timelines')

timeline_service = TimelineService()


@app.route('/', methods=['GET'])
def timelines():
    timelines = timeline_service.get_all()
    return jsonify([timeline.serialize for timeline in timelines]), 200


@app.route('/add', methods=['POST'])
@flask_praetorian.roles_required(*['root'])
def add_timeline():
    req = request.get_json(force=True)
    timeline_service.create(
        title=req.get('title'),
        content=req.get('content')
    )
    return "success", 200


@app.route('/disable', methods=['DELETE'])
@flask_praetorian.roles_required(*['root'])
def disable_timeline():
    req = request.get_json(force=True)
    result = timeline_service.deactive_timeline(id=req.get('timeline_id'))
    if result:
        return 'success', 200
    return 'err', 400

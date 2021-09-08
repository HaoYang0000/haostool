import json
import os
import flask_praetorian
import math
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request, send_from_directory
from flask_api import status
from flask_login import current_user, login_user, logout_user, login_required
from backend.services.backup_restore.backup_restore_service import BackupRestoreService
from backend.engine import session_scope, UPLOAD_ROOT, BACKUP_DIR
from backend.logs.logger import logger
from werkzeug.utils import secure_filename
import uuid

app = Blueprint(
    'backup-restore',
    __name__,
    url_prefix='/api/backup-restore'
)


backup_restore_service = BackupRestoreService()


@app.route('/backups', methods=['GET'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def get_backups():
    backup_rows = backup_restore_service.get_backup_records()
    backup_records = [backup.serialize for backup in backup_rows]
    backup_files = backup_restore_service.get_backup_files()
    output = []

    for backup in backup_files:
        tmp_dict = {}
        tmp_dict['file_name'] = backup
        tmp_dict['records'] = []
        for back_row in backup_records:
            if backup.startswith(back_row['name']):
                tmp_dict['records'].append({
                    "name": back_row['name'],
                    "job_status": back_row['job_status'],
                    "id": back_row['id']
                })
        output.append(tmp_dict)
    return jsonify({
        'backups': output
    }), 200


@app.route('/backups', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def create_backup():
    is_backup_blog = True if request.form['is_backup_blog'] and request.form['is_backup_blog'].lower(
    ) == 'true' else False
    is_backup_video = True if request.form['is_backup_video'] and request.form['is_backup_video'].lower(
    ) == 'true' else False
    is_backup_user_profile = True if request.form['is_backup_user_profile'] and request.form['is_backup_user_profile'].lower(
    ) == 'true' else False
    is_backup_db = True if request.form['is_backup_db'] and request.form['is_backup_db'].lower(
    ) == 'true' else False
    backups = backup_restore_service.create_backup(
        is_backup_blog=is_backup_blog,
        is_backup_video=is_backup_video,
        is_backup_user_profile=is_backup_user_profile,
        is_backup_db=is_backup_db
    )
    return jsonify(backups), 200


@app.route('/backups/record', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_backup_record():
    backup_id = request.form['id'],
    result = backup_restore_service.delete_backup_record(backup_id=backup_id)
    return jsonify(result), 200


@app.route('/backups/record-and-files', methods=['DELETE'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def delete_backup_files():
    name = request.form['name']
    result = backup_restore_service.delete_backup_record(
        name=name, with_file=True)
    return jsonify(result), 200


@app.route('/backups/download', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def download_backup_files():
    file_name = request.form['name']
    dir, file = backup_restore_service.get_backup_file_path(
        file_name=file_name)
    return send_from_directory(directory=dir, filename=file), 200


@app.route('/backups/upload', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def upload_backup_files():
    # check if the post request has the file part
    if 'file' not in request.files:
        logger.error('No file part')
        return 'No file part', 400
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        logger.error('No selected file')
        return 'No selected file', 400

    filename = secure_filename(file.filename)
    file.save(f"{UPLOAD_ROOT}/{BACKUP_DIR}/{filename}")
    return jsonify("success"), 200


@app.route('/restore/record-and-files', methods=['POST'])
@flask_praetorian.roles_accepted(*['root', 'admin'])
def restore_backup_files():
    file_name = request.form['name']
    result = backup_restore_service.restore_record_and_files(
        file_name=file_name)
    return jsonify(result), 200

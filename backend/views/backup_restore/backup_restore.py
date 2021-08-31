import json
import os
import logging
import flask_praetorian
import math
from flask import Blueprint, jsonify, render_template, session, url_for, redirect, flash, request
from flask_api import status
from flask_login import current_user, login_user, logout_user, login_required
from backend.services.backup_restore.backup_restore_service import BackupRestoreService
from backend.engine import session_scope, DEFAULT_PAGE_LIMIT

import uuid

app = Blueprint(
    'backup-restore',
    __name__,
    url_prefix='/api/backup-restore'
)
logger = logging.getLogger(__name__)

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
    backups = backup_restore_service.create_backup()
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


@app.route('/restore/record-and-files', methods=['POST'])
def restore_backup_files():
    file_name = request.form['name']
    result = backup_restore_service.restore_record_and_files(
        file_name=file_name)
    return jsonify(result), 200

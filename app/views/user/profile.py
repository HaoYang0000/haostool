import json
import logging

from flask import Flask, flash, redirect, Blueprint, jsonify, render_template, request, session, abort, url_for
import os
from flask_login import current_user, login_user, logout_user
from app.engine import db, UPLOAD_ROOT, ALLOWED_EXTENSIONS, USER_PROFILE_DIR
from app.forms.user.profile import ProfileForm, IpWhiteListForm, IpAddress
from wtforms.validators import ValidationError
from flask_login import login_required
from app.models.users import UserModel as User
from app.models.user_ip_mapping import UserIpMappingServiceModel as UserIps
from werkzeug.utils import secure_filename
from app.engine import session_scope

app = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)
logger = logging.getLogger(__name__)


@app.route('/profile_setting', methods=['GET'])
@login_required
def profile():
    with session_scope() as session:
        user_ips = session.query(UserIps).filter(UserIps.user_id == current_user.id).all()
        user = session.query(User).filter(User.id == current_user.id).first()

        user_setting_form = ProfileForm()
        ip_white_list_form = IpWhiteListForm()

        for ip in user_ips:
            ip_form = IpAddress()
            ip_form.ip_address = ip.ip_address
            ip_white_list_form.ip_address_list.append_entry(ip_form)
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            current_ip = request.environ['REMOTE_ADDR']
        else:
            current_ip = request.environ['HTTP_X_FORWARDED_FOR']
        return render_template(
            'user/profile.html', 
            user_setting_form=user_setting_form,
            ip_white_list_form=ip_white_list_form, 
            current_ip=current_ip,
            current_user=user
            )


@app.route('/profile_update', methods=['POST'])
@login_required
def profile_update():
    with session_scope() as session:
        user_setting_form = ProfileForm()
        if user_setting_form.validate_on_submit():
            user = session.query(User).filter(User.id == current_user.id).first()
            user.username = user_setting_form.username.data
            user.first_name = user_setting_form.first_name.data
            user.last_name = user_setting_form.last_name.data
            user.nickname = user_setting_form.nickname.data
            user.email = user_setting_form.email.data
            user.phone_num = user_setting_form.phone.data
            if user_setting_form.password.data:
                user.password = User.set_password(user_setting_form.password.data)
            session.commit()
            flash('Congratulations, your profile information is updated! ')
        return redirect(url_for('user.profile'))


@app.route('/ip_white_list_update', methods=['POST'])
@login_required
def ip_white_list_update():
    with session_scope() as session:
        ip_white_list_form = IpWhiteListForm()

        if ip_white_list_form.validate_on_submit():
            for data in ip_white_list_form.ip_address_list.data:
                logger.error(data)
                if len(data['ip_address']) == 0 or data['ip_address'] is None:
                    logger.error("ip is none")
                    continue
                if session.query(UserIps).filter(UserIps.user_id == current_user.id).filter(
                        UserIps.ip_address == data['ip_address']).one_or_none():
                    logger.error("Already exist")
                    continue
                user_ip = UserIps(
                    user_id=current_user.id, ip_address=data['ip_address'])
                session.add(user_ip)
            session.commit()

        return redirect(url_for('user.profile'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['POST'])
def uploaded_file():
    with session_scope() as session:
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('user.profile'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('user.profile'))
        if not allowed_file(file.filename):
            flash('File format not allowed')
            return redirect(url_for('user.profile'))

        filename = secure_filename(file.filename)
        file.save(f"{UPLOAD_ROOT}/{USER_PROFILE_DIR}/{filename}")
        user = session.query(User).filter(User.id == current_user.id).first()
        user.avatar = f"{USER_PROFILE_DIR}/{filename}"
        session.merge(user)
        session.commit()
        flash('File upload successful')
        return redirect(url_for('user.profile'))

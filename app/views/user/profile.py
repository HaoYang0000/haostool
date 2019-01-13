import json
import logging

from flask import Flask, flash, redirect, Blueprint, jsonify, render_template, request, session, abort, url_for
import os
from flask_login import current_user, login_user, logout_user
from app.engine import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from app.forms.user.profile import ProfileForm
from wtforms.validators import ValidationError
from flask_login import login_required
from app.models.users import UserModel as User
from werkzeug.utils import secure_filename
 
app = Blueprint(
    'user',
    __name__,
    url_prefix='/user'
)
logger = logging.getLogger(__name__)
 
@app.route('/profile_setting', methods=['GET'])
@login_required
def profile():
    form = ProfileForm()
    avatar = 'uploads/' + current_user.avatar 
    return render_template('user/profile.html', form=form, current_user=current_user, avatar=avatar)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods=['POST'])
def uploaded_file():
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
	file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), UPLOAD_FOLDER, filename))
	user = db.session.query(User).filter(User.id==current_user.id).first()
	user.avatar = filename
	db.session.commit()
	flash('File upload successful')
	return redirect(url_for('user.profile'))

import json
import logging

from flask import Flask, flash, redirect, Blueprint, jsonify, render_template, request, session, abort, url_for
import os
from flask_login import current_user, login_user, logout_user
from app.engine import db
from app.forms.user.profile import ProfileForm
from wtforms.validators import ValidationError
from flask_login import login_required
from flask import send_from_directory
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
    return render_template('user/profile.html', form=form, current_user=current_user)

UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile_setting', methods=['POST'])
@login_required
def upload_file():
	if request.method == 'POST':
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
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			user = User.query.filter(User.id==current_user.id).one()
			user.avatar = UPLOAD_FOLDER +'/'+filename
			db.session.commit()
			return redirect(url_for('user.profile'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


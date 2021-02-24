import json
import logging
import random
import os
import flask
import flask_praetorian
from flask import Flask, flash, redirect, Blueprint, jsonify, render_template, request, session, abort, url_for, Response
from flask_login import current_user, login_user, logout_user
from backend.models.users.users import UserModel as User
from backend.engine import db, USER_PROFILE_DIR, session_scope, guard, UPLOAD_ROOT
from backend.services.users.user_service import UserService
from flask_login import login_required
from backend.utils.utils import allowed_profile_img_format
from werkzeug.utils import secure_filename


app = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)
logger = logging.getLogger(__name__)
user_service = UserService()


@app.route('/register', methods=['POST'])
def register():
    with session_scope() as ss:
        req = flask.request.get_json(force=True)
        user = User(
            username=req.get('username'),
            first_name=req.get('firstname'),
            last_name=req.get('lastname'),
            nickname=req.get('nickname'),
            email=req.get('email'),
            phone_num=req.get('phonenumber'),
            password=guard.hash_password(req.get('password')),
            avatar=f"{USER_PROFILE_DIR}/random/{random.randint(1,3)}.jpg"
        )
        ss.add(user)
        ss.commit()
        loggedin_user = guard.authenticate(
            req.get('username'), req.get('password'))
        output = {
            "access_token": guard.encode_jwt_token(
                loggedin_user),
            'role': user.rolenames[0] if len(user.rolenames) == 1 else None,
            'user_name': user.username,
            'avatar': user.avatar,
            'id': user.id
        }
        return (flask.jsonify(output), 200)


@app.route('/login', methods=['GET', 'POST'])
def login():
    with session_scope() as ss:
        req = flask.request.get_json(force=True)
        username = req.get('username', None)
        password = req.get('password', None)
        user = guard.authenticate(username, password)
        output = {
            'access_token': guard.encode_jwt_token(
                user),
            'role': user.rolenames[0] if len(user.rolenames) == 1 else None,
            'user_name': user.username,
            'avatar': user.avatar,
            'id': user.id
        }
        return output, 200


@app.route('/update/<int:id>', methods=['POST'])
@flask_praetorian.auth_required
def update(id):
    with session_scope() as ss:
        req = flask.request.get_json(force=True)
        user = user_service.get_by_id(id)
        if req.get('username'):
            user.username = req.get('username')
        if req.get('email'):
            user.email = req.get('email')
        if req.get('password'):
            user.password = guard.hash_password(req.get('password'))
        if req.get('firstname'):
            user.first_name = req.get('firstname')
        if req.get('lastname'):
            user.last_name = req.get('lastname')
        if req.get('nickname'):
            user.nickname = req.get('nickname')
        if req.get('phonenum'):
            user.phone_num = req.get('phonenum')
        ss.add(user)
        ss.commit()
        return "success", 200


@app.route('/update-profile-img/<int:id>', methods=['POST'])
@flask_praetorian.auth_required
def update_profile_img(id):
    with session_scope() as session:
        # check if the post request has the file part
        if 'file' not in request.files:
            logger.error('No file part')
            return "nah", 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            logger.error('No selected file')
            return "nah", 400
        if not allowed_profile_img_format(file.filename):
            logger.error('File format not allowed')
            return "nah", 400

        filename = secure_filename(file.filename)
        file.save(f"{UPLOAD_ROOT}/{USER_PROFILE_DIR}/{filename}")
        user = user_service.get_by_id(id)
        user.avatar = f"{USER_PROFILE_DIR}/{filename}"
        session.merge(user)
        session.commit()
        return "success", 200


@app.route('/get-user/<int:id>', methods=['GET'])
@flask_praetorian.auth_required
def get_user(id):
    with session_scope() as ss:
        user = user_service.get_by_id(id)
        return user.serialize, 200


@app.route('/refresh', methods=['POST'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    .. example::
       $ curl http://localhost:5000/api/refresh -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    print("refresh request")
    old_token = request.get_data()
    new_token = guard.refresh_jwt_token(old_token)
    ret = {'access_token': new_token}
    return ret, 200


@app.route('/protected')
@flask_praetorian.auth_required
def protected():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}


@app.route('/adminrequired')
@flask_praetorian.roles_required('admin')
def admin_required():
    """
    A protected endpoint. The auth_required decorator will require a header
    containing a valid JWT
    .. example::
       $ curl http://localhost:5000/api/protected -X GET \
         -H "Authorization: Bearer <your_token>"
    """
    return {'message': f'protected endpoint (allowed user {flask_praetorian.current_user().username})'}

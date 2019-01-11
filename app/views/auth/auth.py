import json
import logging

from flask import Flask, flash, redirect, Blueprint, jsonify, render_template, request, session, abort, url_for
import os
from flask_login import current_user, login_user, logout_user
from app.models.users import UserModel as User
from app.engine import db
from app.forms.auth.auth_forms import RegistrationForm, LoginForm
from wtforms.validators import ValidationError
 
app = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)
logger = logging.getLogger(__name__)
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username==form.username.data) | (User.email==form.username.data)).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        session['logged_in'] = True
        login_user(user, remember=form.rememberme.data)
        return redirect(url_for('index.main'))
    return render_template('auth/login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    logout_user()
    return redirect(url_for('index.main'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        session['logged_in'] = True
        return redirect(url_for('index.main'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        session['logged_in'] = True
        login_user(user, remember=form.rememberme.data)
        return redirect(url_for('index.main'))
    return render_template('auth/register.html', title='Register', form=form)

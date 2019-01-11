from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class ProfileForm(FlaskForm):
	avatar = PasswordField('Avatar:', validators=[])
	username = StringField('Username:', validators=[DataRequired()])
	first_name = StringField('First Name:', validators=[DataRequired()])
	last_name = StringField('Last Name:', validators=[DataRequired()])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	password = PasswordField('Password:', validators=[DataRequired()])
	submit = SubmitField('Update')

	


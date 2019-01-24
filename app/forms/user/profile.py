from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


class ProfileForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[])
    submit = SubmitField('Update')

class IpAddress(FlaskForm):
    ip_address = StringField('Ip adress:', validators=[])

class IpWhiteListForm(FlaskForm):
    ip_address_list = FieldList(FormField(IpAddress), min_entries=1)
    submit = SubmitField('Update')

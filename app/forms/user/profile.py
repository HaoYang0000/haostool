from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _

class ProfileForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    first_name = StringField(_('First Name'), validators=[DataRequired()])
    last_name = StringField(_('Last Name'), validators=[DataRequired()])
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    phone = StringField(_('Phone'))
    password = PasswordField(_('Password'), validators=[])
    submit = SubmitField(_('Update'))

class IpAddress(FlaskForm):
    ip_address = StringField('Ip adress', validators=[])

class IpWhiteListForm(FlaskForm):
    ip_address_list = FieldList(FormField(IpAddress), min_entries=1)
    submit = SubmitField('Update')

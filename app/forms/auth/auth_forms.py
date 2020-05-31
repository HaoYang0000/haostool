from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.users import UserModel as User
from flask_babel import lazy_gettext as _

class RegistrationForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    first_name = StringField(_('First Name'))
    last_name = StringField(_('Last Name'))
    email = StringField(_('Email'), validators=[DataRequired(), Email()])
    phone = StringField(_('Phone number'))
    password = PasswordField(_('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    rememberme = BooleanField(_('RememberMe'))
    submit = SubmitField(_('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))

class LoginForm(FlaskForm):
    username = StringField(_('Username'), validators=[DataRequired()])
    password = PasswordField(_('Password'), validators=[DataRequired()])

    rememberme = BooleanField(_('RememberMe'))
    submit = SubmitField(_('Login'))
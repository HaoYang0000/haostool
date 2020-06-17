from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _

class VideoCommentForm(FlaskForm):
    unknown_user_name = StringField(_('Username:'))
    content = TextAreaField(_('Content'), validators=[DataRequired()])
    video_uuid = StringField('video_uuid')
    category = 'video'
    submit = SubmitField(_('Post'))
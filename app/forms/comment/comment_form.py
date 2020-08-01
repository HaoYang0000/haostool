from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _

class CommentForm(FlaskForm):
    unknown_user_name = StringField(_('Username:'))
    content = TextAreaField(_('Content'), validators=[DataRequired()])
    video_uuid = StringField('video_uuid')
    blog_uuid = StringField('blog_uuid')
    category = 'video'
    submit = SubmitField(_('Post'))
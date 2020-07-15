from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DateField, SelectField, TextAreaField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from flask_babel import lazy_gettext as _
import datetime

class CreateBlogPostForm(FlaskForm):
    title = StringField(label=_('title'), validators=[DataRequired()])
    cover_img = FileField(label=_('cover img'), id="cover_img")
    blog_intro = TextAreaField(label=_('intro'), id="blog_intro")
    content = TextAreaField(label=_('content'), id="text_editor")
    submit = SubmitField('Post')



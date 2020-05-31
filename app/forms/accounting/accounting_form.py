from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import lazy_gettext as _
import datetime

class AddItemForm(FlaskForm):
    item_name = StringField(_('Item Name:'), validators=[DataRequired()])
    item_price = FloatField(_('Item Price:'), validators=[DataRequired()])
    item_date = DateField(_('Purchase Date:'), validators=[DataRequired()], format='%Y-%m-%d', default=datetime.date.today())
    tag_id = SelectField(_('Tag:'), coerce=int, validators=[DataRequired()])
    submit = SubmitField(_('Add'))

class AddTagForm(FlaskForm):
    tag_name = StringField(_('Tag Name:'), validators=[DataRequired()])
    submit = SubmitField(_('Add'))

class AddCategoryForm(FlaskForm):
    category_name = StringField(_('Category Name:'), validators=[DataRequired()])
    tag_id = StringField(_('Tag:'), validators=[DataRequired()])
    submit = SubmitField(_('Add'))
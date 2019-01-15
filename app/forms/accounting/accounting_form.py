from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import datetime

class AddItemForm(FlaskForm):
    item_name = StringField('Item Name:', validators=[DataRequired()])
    item_price = FloatField('Item Price:', validators=[DataRequired()])
    item_date = DateField('Purchase Date:', validators=[DataRequired()], format='%Y-%m-%d', default=datetime.date.today())
    tag_id = SelectField('Tag:', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Add')

class AddTagForm(FlaskForm):
    tag_name = StringField('Tag Name:', validators=[DataRequired()])
    submit = SubmitField('Add')

class AddCategoryForm(FlaskForm):
    category_name = StringField('Category Name:', validators=[DataRequired()])
    tag_id = StringField('Tag:', validators=[DataRequired()])
    submit = SubmitField('Add')
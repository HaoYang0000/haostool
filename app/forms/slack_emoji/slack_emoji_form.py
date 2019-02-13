from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, TextAreaField

class SlackEmojiForm(FlaskForm):
    emoji = StringField('emoji:', default=':dealwithit:')
    padding = StringField('padding:', default=':white_large_square:')
    input = StringField('Input string:')
    if_same_line = BooleanField('If show all word on same line:')
    if_reverse = BooleanField('If reverse padding and emoji:')
    generated_output = TextAreaField("generated_output", default="Select the options and wait for magic")
    submit = SubmitField('Generate')

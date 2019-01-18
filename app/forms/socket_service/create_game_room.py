from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models.socket_service.game_room import GameRoomModel
import datetime

class CreateGameRoomForm(FlaskForm):
    name = StringField('Room Name:', validators=[DataRequired()])
    expire_at = DateField('Expire at', validators=[DataRequired()], format='%Y-%m-%d', default=datetime.date.today() + datetime.timedelta(days=1))
    submit = SubmitField('Create')

    def validate_room(self, name):
        room = GameRoomModel.query.filter_by(name=name.data).first()
        if room is not None:
            raise ValidationError('Please use a different room name.')

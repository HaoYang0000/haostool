from app.models.users import UserModel
from .base import BaseMeta, BaseSchema
from marshmallow import fields


class UserSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = UserModel

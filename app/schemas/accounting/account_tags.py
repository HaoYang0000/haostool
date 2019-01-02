from app.models.account_tags import AccountTagModel
from .base import BaseMeta, BaseSchema
from marshmallow import fields

class AccountTagSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = AccountTagModel

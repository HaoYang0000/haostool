from app.models.accounting.account_tags import AccountTagModel
from app.schemas.base import BaseMeta, BaseSchema
from marshmallow import fields

class AccountTagSchema(BaseSchema):
    id = fields.Integer(dump_only=True)
    cost = fields.Float(required=False)

    class Meta(BaseMeta):
        model = AccountTagModel
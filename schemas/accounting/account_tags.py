from models.accounting.account_tags import AccountTagModel
from schemas.base import BaseMeta, BaseSchema
from marshmallow import fields

class AccountTagSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = AccountTagModel

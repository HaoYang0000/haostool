from app.models.accounting.account_items import AccountItemModel
from .base import BaseMeta, BaseSchema
from marshmallow import fields

class AccountItenSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = AccountItemModel

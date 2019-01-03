from app.models.accounting.account_items import AccountItemModel
from app.schemas.base import BaseMeta, BaseSchema
from marshmallow import fields

class AccountItemSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = AccountItemModel

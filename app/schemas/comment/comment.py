from app.models.comment import CommentModel
from app.schemas.base import BaseMeta, BaseSchema
from marshmallow import fields


class CommentSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = CommentModel

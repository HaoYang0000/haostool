from marshmallow import post_dump
from marshmallow_sqlalchemy import ModelSchema
from app.main import db


class BaseSchema(ModelSchema):
    def __init__(self, wrap=True, *args, **kwargs):
        self.wrap = wrap
        super().__init__(*args, **kwargs)

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, _):
        if self.wrap:
            return {"result": data}
        else:
            return data


class BaseMeta:
    include_fk = True
    dateformat = DATE_FORMAT
    sqla_session = db.session
    strict = True

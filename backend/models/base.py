from sqlalchemy import Column, text, DateTime, Integer
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    __table_args__ = (
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci',
            'extend_existing': True
        }
    )


class BaseModelExtended(BaseModel):
    __abstract__ = True

    """
    This will function as a shared base for new tables moving forward to keep table structure consistent.
    For now, we are adding an id PK, created_at, and updated_at by default.
    In the future, we should also use this to add soft delete to all models
    """
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )


class BaseSchema(ModelSchema):
    def __init__(self, wrap=True, *args, **kwargs):
        self.wrap = wrap
        super().__init__(*args, **kwargs)


class BaseMeta:
    include_fk = True
    datetimeformat = '%Y-%m-%d %H:%M:%S'
    sqla_session = db.session
    strict = True

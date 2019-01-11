from sqlalchemy import Column, text, DateTime, Integer
import config
from flask_sqlalchemy import SQLAlchemy
# from app.engine import db

db = SQLAlchemy()

class BaseModel(db.Model):
    __abstract__ = True

    __table_args__ = (
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8mb4',
            'mysql_collate': 'utf8mb4_unicode_ci'
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

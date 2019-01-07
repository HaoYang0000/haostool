from main import db
from models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text


class AccountTagModel(BaseModelExtended):
    __tablename__ = 'account_tags'

    name = Column(
        String(length=255),
        nullable=False
    )

    def __repr__(self):
        return (
            "AccountTagModel(\
            id='{id}', \
            name='{name}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

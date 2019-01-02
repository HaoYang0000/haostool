from app.main import db
from app.models.base import BaseModelExtended
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
            created_by='{created_by}', \
            updated_by='{updated_by}')"
        ).format(
            id=self.id,
            name=self.name,
            created_by=self.created_by,
            updated_by=self.updated_by
        )

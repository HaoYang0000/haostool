from app.main import db
from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float


class AccountItemModel(BaseModelExtended):
    __tablename__ = 'account_items'

    name = Column(
        String(length=255),
        nullable=False
    )

    price = Column(
        Float,
        nullable=False
    )

    date = Column(
    	DateTime,
        nullable=False
    )

    tag_id = Column(
        Integer,
        ForeignKey('account_tags.id', name='fk_accounting_tag_id'),
        nullable=False
    )

    def __repr__(self):
        return (
            "AccountItemModel(\
            id='{id}', \
            name='{name}', \
            price='{price}', \
            date='{date}', \
            created_by='{created_by}', \
            updated_by='{updated_by}')"
        ).format(
            id=self.id,
            name=self.name,
            price=self.price,
            date=self.date,
            created_by=self.created_by,
            updated_by=self.updated_by
        )

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

    user_id = Column(
        Integer,
        ForeignKey('users.id', name='fk_accounting_item_user_id'),
        nullable=False
    )

    def __repr__(self):
        return (
            "AccountItemModel(\
            id='{id}', \
            name='{name}', \
            price='{price}', \
            date='{date}', \
            user_id='{user_id}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            name=self.name,
            price=self.price,
            date=self.date,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

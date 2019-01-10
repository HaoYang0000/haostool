from models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text


class AccountTagModel(BaseModelExtended):
    __tablename__ = 'account_tags'

    name = Column(
        String(length=255),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id', name='fk_accounting_tag_user_id'),
        nullable=False
    )

    def __repr__(self):
        return (
            "AccountTagModel(\
            id='{id}', \
            name='{name}', \
            user_id='{user_id}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            name=self.name,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

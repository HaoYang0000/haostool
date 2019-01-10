from models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float


class AccountCategoryModel(BaseModelExtended):
    __tablename__ = 'account_categories'

    name = Column(
        String(length=255),
        nullable=False
    )

    tag_id = Column(
        Integer,
        ForeignKey('account_tags.id', name='fk_accounting_tag_category_id'),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id', name='fk_accounting_cate_user_id'),
        nullable=False
    )

    def __repr__(self):
        return (
            "AccountCategoryModel(\
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

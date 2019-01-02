from app.main import db
from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text


class UserModel(BaseModelExtended):
    __tablename__ = 'users'

    email = Column(
        String(length=255),
        nullable=False
    )
    
    password = Column(
        String(length=255),
        nullable=False
    )

    username = Column(
        String(length=255),
        nullable=False
    )

    avatar = Column(
        String(length=255),
        nullable=True
    )

    def __repr__(self):
        return (
            "UserModel(\
            id='{id}', \
            email='{email}', \
            password='{password}', \
            username='{username}', \
            avatar='{avatar}' \
            created_by='{created_by}', \
            updated_by='{updated_by}')"
        ).format(
            id=self.id,
            email=self.email,
            password=self.password,
            username=self.username,
            avatar=self.avatar,
            created_by=self.created_by,
            updated_by=self.updated_by
        )

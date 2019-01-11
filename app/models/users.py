from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.engine import login_manager

class UserModel(UserMixin, BaseModelExtended):
    __tablename__ = 'users'

    email = Column(
        String(length=255),
        nullable=False
    )
    
    password = Column(
        String(length=255),
        nullable=False
    )

    first_name = Column(
        String(length=255),
        nullable=False
    )

    last_name = Column(
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

    is_active = Column(
        Boolean(),
        default=True
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @login_manager.user_loader
    def load_user(id):
        return UserModel.query.get(int(id))
    
    def __repr__(self):
        return (
            "UserModel(\
            id='{id}', \
            email='{email}', \
            password='{password}', \
            username='{username}', \
            first_name='{first_name}', \
            last_namelast_name='{last_name}', \
            avatar='{avatar}', \
            is_active='{is_active}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            email=self.email,
            password=self.password,
            username=self.username,
            first_namefirst_name=self.first_name,
            last_name=self.last_name,
            avatar=self.avatar,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

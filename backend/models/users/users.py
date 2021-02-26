from backend.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text
from flask_login import UserMixin
from sqlalchemy import or_


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

    gesture_hash = Column(
        String(length=255),
        nullable=True
    )

    first_name = Column(
        String(length=255),
        nullable=True
    )

    last_name = Column(
        String(length=255),
        nullable=True
    )

    username = Column(
        String(length=255),
        nullable=False
    )

    nickname = Column(
        String(length=255),
        nullable=True
    )

    phone_num = Column(
        String(length=255),
        nullable=True
    )

    avatar = Column(
        String(length=255),
        nullable=True
    )

    # 0: root
    # 1: aadmin
    # 2: normal
    level = Column(
        Integer,
        default=2
    )

    is_active = Column(
        Boolean(),
        default=True
    )

    @property
    def rolenames(self):
        try:
            if self.level == 0:
                return ["root"]
            elif self.level == 1:
                return ["admin"]
            elif self.level == 2:
                return ["normal"]
            return []
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter(or_(cls.username == username, cls.email == username)).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nickname': self.nickname,
            'phone_num': self.phone_num,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return (
            "UserModel(\
            id='{id}', \
            email='{email}', \
            password='{password}', \
            username='{username}', \
            first_name='{first_name}', \
            last_name='{last_name}', \
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

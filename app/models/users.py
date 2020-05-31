from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.engine import login_manager, db
from app.models.user_ip_mapping import UserIpMappingServiceModel

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

    ip_addresses = db.relationship('UserIpMappingServiceModel', backref='users', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def check_gesture_hash(self, gesture_list):
        return check_password_hash(self.gesture_hash, str(gesture_list))
    
    @staticmethod
    def generate_gesture_hash(gesture_list):
        return generate_password_hash(str(gesture_list))

    @login_manager.user_loader
    def load_user(id):
        return UserModel.query.get(int(id))
    
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
            'avatar': self.avatar,
            'ip_addresses': self.ip_addresses,
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
            ip_addresses='{ip_addresses}', \
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
            ip_addresses=self.ip_addresses,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash


class UserIpMappingServiceModel(BaseModelExtended):
    __tablename__ = 'user_ip_mapping'

    user_id = Column(
        Integer,
        ForeignKey('users.id', name='fk_service_user_id'),
        nullable=False
    )

    ip_address = Column(
        String(length=255),
        nullable=False
    )

    def __repr__(self):
        return (
            "UserIpMappingServiceModel(\
            id='{id}', \
            user_id='{user_id}', \
            ip_address='{ip_address}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            user_id=self.user_id,
            ip_address=self.ip_address,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

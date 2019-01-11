from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash

class UserServiceModel(BaseModelExtended):
    __tablename__ = 'user_service'

    user_id = Column(
        Integer,
        ForeignKey('users.id', name='fk_service_user_id'),
        nullable=False
    )
    
    service_id = Column(
        Integer,
        ForeignKey('services.id', name='fk_service_services_id'),
        nullable=False
    )

    
    def __repr__(self):
        return (
            "UserServiceModel(\
            id='{id}', \
            user_id='{user_id}', \
            service_id='{service_id}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

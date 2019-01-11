from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text
from werkzeug.security import generate_password_hash, check_password_hash

class ServiceModel(BaseModelExtended):
    __tablename__ = 'services'

    name = Column(
        String(length=255),
        nullable=False
    )
    
    base_url = Column(
        String(length=255),
        nullable=False
    )

    description = Column(
        String(length=255),
        nullable=False
    )

    is_active = Column(
        Boolean(),
        default=True
    )
    
    def __repr__(self):
        return (
            "ServiceModel(\
            id='{id}', \
            name='{name}', \
            base_url='{base_url}', \
            description='{description}', \
            is_active='{is_active}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            name=self.name,
            base_url=self.base_url,
            description=self.description,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

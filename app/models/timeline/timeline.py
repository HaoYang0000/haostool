from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, Enum, String
from sqlalchemy.orm import relationship

class TimelineModel(BaseModelExtended):
    __tablename__ = 'timelines'

    message = Column(
        String(length=255),
        nullable=False
    )

    url = Column(
        String(length=255),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )


    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'message': self.message,
            'url': self.url,
            'is_active': self.is_active
        }

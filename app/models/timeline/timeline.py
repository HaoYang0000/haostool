from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, Enum, String
from sqlalchemy.orm import relationship

class TimelineModel(BaseModelExtended):
    __tablename__ = 'timelines'

    title = Column(
        String(length=255),
        nullable=False
    )

    content = Column(
        String(length=2000),
        nullable=False
    )

    url = Column(
        String(length=255),
        nullable=True
    )

    is_removed = Column(
        Boolean,
        default=False
    )


    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'is_removed': self.is_removed
        }

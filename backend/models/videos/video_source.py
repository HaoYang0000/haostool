from backend.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, Enum, String
from sqlalchemy.orm import relationship


class VideoSourceModel(BaseModelExtended):
    __tablename__ = 'video_source'

    name = Column(
        String(length=255),
        nullable=False
    )

    url = Column(
        String(length=255),
        nullable=False
    )

    icon = Column(
        String(length=255),
        nullable=True
    )

    video_id = Column(
        Integer,
        ForeignKey('videos.id'),
        nullable=False
    )

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'icon': self.icon
        }

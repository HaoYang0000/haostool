from backend.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, Enum, String
from sqlalchemy.orm import relationship


class LabelModel(BaseModelExtended):
    __tablename__ = 'labels'

    name = Column(
        String(length=255),
        nullable=False
    )

    blogs = relationship(
        "BlogPostModel", secondary="label_bridges", lazy='subquery')
    videos = relationship(
        "VideoModel", secondary="label_bridges", lazy='subquery')

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at
        }

from backend.models.base import BaseMeta, BaseModelExtended, BaseSchema
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float, Text, Enum
from marshmallow import fields
from sqlalchemy.orm import relationship
from backend.models.labels.label import LabelModel
from backend.models.labels.label_bridge import LabelBridgeModel
from backend.models.videos.video_source import VideoSourceModel


class VideoModel(BaseModelExtended):
    __tablename__ = 'videos'

    title = Column(
        String(length=255),
        nullable=False
    )

    path = Column(
        String(length=255),
        nullable=False
    )

    thumb_nail = Column(
        String(length=255),
        nullable=False
    )

    uuid = Column(
        String(length=255),
        default=False
    )

    liked_number = Column(
        Integer,
        default=0
    )

    viewed_number = Column(
        Integer,
        default=0
    )

    star = Column(
        Integer,
        default=1
    )
    category = Column(
        Enum('dota', 'pubg', 'fallguys', 'blog', 'piano', 'sax'),
        nullable=False
    )

    labels = relationship(
        "LabelModel", secondary='label_bridges', lazy='subquery')

    sources = relationship("VideoSourceModel", lazy='subquery')

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'title': self.title,
            'path': self.path,
            'thumb_nail': self.thumb_nail,
            'uuid': self.uuid,
            'liked_number': self.liked_number,
            'viewed_number': self.viewed_number,
            'star': self.star,
            'labels': [label.serialize for label in self.labels],
            'sources': [source.serialize for source in self.sources],
            'category': self.category,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


# class VideoModelSchema(BaseSchema):
#     id = fields.Integer(dump_only=True)

#     class Meta(BaseMeta):
#         model = VideoModel

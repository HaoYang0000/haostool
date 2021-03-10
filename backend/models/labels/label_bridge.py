from backend.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, Enum, String
from sqlalchemy.orm import relationship, backref


class LabelBridgeModel(BaseModelExtended):
    __tablename__ = 'label_bridges'

    label_id = Column(
        Integer,
        ForeignKey('labels.id'),
        nullable=True
    )

    blog_id = Column(
        Integer,
        ForeignKey('blog_posts.id'),
        nullable=True
    )

    video_id = Column(
        Integer,
        ForeignKey('videos.id'),
        nullable=True
    )

    labels = relationship(
        "backend.models.labels.label.LabelModel", backref=backref("label_bridges", cascade="all, delete-orphan"))
    blogs = relationship(
        "backend.models.blogs.post.BlogPostModel", backref=backref("label_bridges", cascade="all, delete-orphan"))
    videos = relationship(
        "backend.models.videos.video.VideoModel", backref=backref("label_bridges", cascade="all, delete-orphan"))

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'blog_id': self.blog_id,
            'video_id': self.video_id,
            'created_at': self.created_at
        }

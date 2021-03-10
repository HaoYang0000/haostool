from backend.models.base import BaseMeta, BaseModelExtended, BaseSchema
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float, Text
from marshmallow import fields
from sqlalchemy.orm import relationship
from backend.models.labels.label import LabelModel
from backend.models.labels.label_bridge import LabelBridgeModel


class BlogPostModel(BaseModelExtended):
    __tablename__ = 'blog_posts'

    title = Column(
        String(length=255),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    is_published = Column(
        Boolean(),
        default=False
    )

    liked_number = Column(
        Integer,
        default=0
    )

    blog_intro = Column(
        Text,
        nullable=False
    )

    cover_img = Column(
        String(length=255),
        nullable=False
    )

    viewed_number = Column(
        Integer,
        default=0
    )

    uuid = Column(
        String(length=255),
        nullable=False
    )

    labels = relationship(
        "LabelModel", secondary='label_bridges', lazy='subquery')

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'is_published': self.is_published,
            'liked_number': self.liked_number,
            'viewed_number': self.viewed_number,
            'uuid': self.uuid,
            'cover_img': self.cover_img,
            'blog_intro': self.blog_intro,
            'labels': [label.serialize for label in self.labels],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BlogPostModelSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = BlogPostModel

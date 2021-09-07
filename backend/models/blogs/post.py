from backend.models.base import BaseMeta, BaseModelExtended, BaseSchema
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float, Text
from marshmallow import fields
from sqlalchemy.orm import relationship, backref
from backend.models.labels.label import LabelModel
from backend.models.labels.label_bridge import LabelBridgeModel
from backend.models.users.users import UserModel


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

    is_hidden = Column(
        Boolean(),
        default=False
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
            'is_hidden': self.is_hidden,
            'liked_number': self.liked_number,
            'viewed_number': self.viewed_number,
            'uuid': self.uuid,
            'cover_img': self.cover_img,
            'blog_intro': self.blog_intro,
            'labels': [label.serialize for label in self.labels],
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class HiddenContentModel(BaseModelExtended):
    __tablename__ = 'hidden_content'

    name = Column(
        String(length=255),
        nullable=False
    )

    uuid = Column(
        String(length=255),
        nullable=False
    )

    users = relationship(
        "UserModel", secondary="hidden_content_bridges", lazy='subquery')
    blogs = relationship(
        "backend.models.blogs.post.BlogPostModel", secondary="hidden_content_bridges", lazy='subquery')

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'name': self.name,
            'blogs': [blog.serialize for blog in self.blogs],
            'uuid': self.uuid
        }


class HiddenContentBridgeModel(BaseModelExtended):
    __tablename__ = 'hidden_content_bridges'

    hidden_content_id = Column(
        Integer,
        ForeignKey('hidden_content.id'),
        nullable=False
    )

    blog_id = Column(
        Integer,
        ForeignKey('blog_posts.id'),
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=True
    )

    labels = relationship("HiddenContentModel", backref=backref(
        "hidden_content_bridges", cascade="all, delete-orphan"))
    blogs = relationship("BlogPostModel", backref=backref(
        "hidden_content_bridges", cascade="all, delete-orphan"))
    users = relationship("UserModel", backref=backref(
        "hidden_content_bridges", cascade="all, delete-orphan"))

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'hidden_content_id': self.hidden_content_id,
            'blog_id': self.blog_id,
            'user_id': self.user_id,
            'created_at': self.created_at
        }

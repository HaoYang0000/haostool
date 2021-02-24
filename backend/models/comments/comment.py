from backend.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, Integer, DateTime, Text, Enum, String
from sqlalchemy.orm import relationship
from backend.models.users.users import UserModel


class CommentModel(BaseModelExtended):
    __tablename__ = 'comments'

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=True
    )

    unknown_user_name = Column(
        String(length=255),
        nullable=True
    )

    contact_email = Column(
        String(length=255),
        nullable=True
    )

    content = Column(
        Text,
        nullable=False
    )

    reply_id = Column(
        Integer,
        nullable=True
    )

    category = Column(
        Enum('video', 'blog', 'feedback'),
        nullable=False
    )

    video_uuid = Column(
        String(length=225),
        nullable=True
    )

    blog_uuid = Column(
        String(length=225),
        nullable=True
    )

    is_removed = Column(
        Boolean,
        default=False
    )

    user = relationship("UserModel", lazy='subquery')

    @property
    def serialize(self):
        ""
        "Return object data in easily serializeable format"
        ""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.serialize if self.user else None,
            'unknown_user_name': self.unknown_user_name,
            'content': self.content,
            'reply_id': self.reply_id,
            'category': self.category,
            'video_uuid': self.video_uuid,
            'blog_uuid': self.blog_uuid,
            'is_removed': self.is_removed,
            'created_at': self.created_at
        }

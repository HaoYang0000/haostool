from app.models.base import BaseModelExtended
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float


class GameRoomModel(BaseModelExtended):
    __tablename__ = 'game_rooms'

    name = Column(
        String(length=255),
        nullable=False
    )

    uuid = Column(
        String,
        nullable=False
    )

    expire_at = Column(
    	DateTime,
        nullable=False
    )

    def __repr__(self):
        return (
            "GameRoomModel(\
            id='{id}', \
            name='{name}', \
            uuid='{uuid}', \
            expire_at='{expire_at}', \
            created_at='{created_at}', \
            updated_at='{updated_at}')"
        ).format(
            id=self.id,
            name=self.name,
            uuid=self.uuid,
            expire_at=self.expire_at,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

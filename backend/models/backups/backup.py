from backend.models.base import BaseMeta, BaseModelExtended, BaseSchema
from sqlalchemy import Column, ForeignKey, Boolean, String, Integer, DateTime, Text, Float, Text
from marshmallow import fields


class BackupModel(BaseModelExtended):
    __tablename__ = 'backups'

    name = Column(
        String(length=255),
        nullable=False
    )

    job_status = Column(
        Text,
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
            'job_status': self.job_status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BackupModelSchema(BaseSchema):
    id = fields.Integer(dump_only=True)

    class Meta(BaseMeta):
        model = BackupModel

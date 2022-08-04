from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declared_attr

from src.utils.utils import equals


class AbstractEntity(object):
    entity_status = Column(
        postgresql.ENUM("ACTIVE", "DELETE", name="status_enum", created_type=False),
        nullable=False,
    )
    created_date = Column(DateTime(), default=datetime.now())
    updated_date = Column(DateTime(), default=datetime.now())
    created = None
    updated = None

    @declared_attr
    def created_by(self):
        return Column(
            Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )

    @declared_attr
    def updated_by(self):
        return Column(
            Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )

    def __eq__(self, other):
        return equals(self, other)

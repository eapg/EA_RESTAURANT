# class to process the clients orders
from src.utils.utils import equals
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer(), primary_key=True, nullable=False)
    status = Column(
        postgresql.ENUM(
            "NEW_ORDER",
            "IN_PROCESS",
            "COMPLETED",
            "CANCELLED",
            name="order_status_enum",
            create_type=False,
        )
    )
    assigned_chef_id = Column(
        Integer(), ForeignKey("chef.id", ondelete="CASCADE"), nullable=False
    )
    client_id = Column(
        Integer(), ForeignKey("client.id", ondelete="CASCADE"), nullable=False
    )
    entity_status = Column(
        postgresql.ENUM("ACTIVE", "DELETE", name="status_enum", create_type=False),
        nullable=False,
    )
    create_by = Column(
        Integer(), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    create_date = Column(DateTime(), default=datetime.now())
    update_by = Column(
        Integer(), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    update_date = Column(DateTime(), default=datetime.now())

    chef = relationship("Chef", backref="orders")
    client = relationship("Client", backref="orders")
    user = relationship("User", backref="orders")
    order_detail = relationship("OrderDetail", back_populates="orders")

    def __eq__(self, other):
        return equals(self, other)

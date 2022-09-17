from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import AbstractConcreteBase, declarative_base
from sqlalchemy.orm import declared_attr, relationship

from src.lib.entities.chef import Chef as ChefBase
from src.lib.entities.client import Client as ClientBase
from src.lib.entities.ingredient import Ingredient as IngredientBase
from src.lib.entities.inventory import Inventory as InventoryBase
from src.lib.entities.inventory_ingredient import \
    InventoryIngredient as InventoryIngredientBase
from src.lib.entities.order import Order as OrderBase
from src.lib.entities.order_detail import OrderDetail as OrderDetailBase
from src.lib.entities.order_status_history import \
    OrderStatusHistory as OrderStatusHistoryBase
from src.lib.entities.product import Product as ProductBase
from src.lib.entities.product_ingredient import \
    ProductIngredient as ProductIngredientBase
from src.lib.entities.user import User as UserBase

Base = declarative_base()


class AbstractEntity(Base, AbstractConcreteBase):
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
        return Column(Integer(), ForeignKey("users.id"), nullable=False)

    @declared_attr
    def updated_by(self):
        return Column(Integer(), ForeignKey("users.id"), nullable=False)


class Chef(AbstractEntity, ChefBase):
    __tablename__ = "chefs"

    id = Column(Integer(), primary_key=True, nullable=False)
    user_id = Column(
        Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    skill = Column(Integer(), nullable=False)
    user = None


class Client(AbstractEntity, ClientBase):
    __tablename__ = "clients"

    id = Column(Integer(), primary_key=True, nullable=False)
    user_id = Column(
        Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = None


class Ingredient(AbstractEntity, IngredientBase):
    __tablename__ = "ingredients"

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False)
    description = Column(String(length=100), nullable=False)


class InventoryIngredient(AbstractEntity, InventoryIngredientBase):
    __tablename__ = "inventory_ingredients"

    id = Column(Integer(), primary_key=True, nullable=False)
    ingredient_id = Column(
        Integer(), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    inventory_id = Column(
        Integer(), ForeignKey("inventories.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer(), nullable=False)
    ingredient = None
    inventory = None


class Inventory(AbstractEntity, InventoryBase):
    __tablename__ = "inventories"

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False)


class Order(AbstractEntity, OrderBase):
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
        Integer(), ForeignKey("chefs.id", ondelete="CASCADE"), nullable=False
    )
    client_id = Column(
        Integer(), ForeignKey("clients.id", ondelete="CASCADE"), nullable=False
    )
    chef = None
    client = None


class OrderDetail(AbstractEntity, OrderDetailBase):
    __tablename__ = "order_details"

    id = Column(Integer(), primary_key=True, nullable=False)
    order_id = Column(
        Integer(), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer(), ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer(), nullable=False)
    product = None
    order = None


class OrderStatusHistory(AbstractEntity, OrderStatusHistoryBase):
    __tablename__ = "order_status_histories"

    id = Column(Integer(), primary_key=True, nullable=False)
    order_id = Column(
        Integer(), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    from_time = Column(DateTime())
    to_time = Column(DateTime())
    from_status = Column(
        postgresql.ENUM(
            "NEW_ORDER",
            "IN_PROCESS",
            "COMPLETED",
            "CANCELLED",
            name="order_status_enum",
            create_type=False,
        )
    )
    to_status = Column(
        postgresql.ENUM(
            "NEW_ORDER",
            "IN_PROCESS",
            "COMPLETED",
            "CANCELLED",
            name="order_status_enum",
            create_type=False,
        )
    )
    etl_status = Column(String(length=50))
    order = None


class Product(AbstractEntity, ProductBase):
    __tablename__ = "products"

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False)
    description = Column(String(length=100), nullable=False)


class ProductIngredient(AbstractEntity, ProductIngredientBase):
    __tablename__ = "product_ingredients"

    id = Column(Integer(), primary_key=True, nullable=False)
    product_id = Column(
        Integer(), ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    ingredient_id = Column(
        Integer(), ForeignKey("ingredients.id", ondelete="CASCADE"), nullable=False
    )
    quantity = Column(Integer(), nullable=False)
    cooking_type = Column(
        postgresql.ENUM(
            "ADDING",
            "ROASTING",
            "BOILING",
            "BAKING",
            "FRYING",
            "HEADING",
            "PREPARING_DRINK",
            name="cooking_type_enum",
            create_type=False,
        ),
        nullable=False,
    )
    product = None
    ingredient = None


class User(AbstractEntity, UserBase):
    __tablename__ = "users"
    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(length=50), nullable=False)
    last_name = Column(String(length=50), nullable=False)
    user_name = Column(String(length=50), nullable=False)
    password = Column(String(length=500), nullable=False)
    role = Column(
        postgresql.ENUM(
            "CHEF",
            "CLIENT",
            "CASHIER",
            "SEEDER",
            "KITCHEN_SIMULATOR",
            name="user_role_enum",
            create_type=False,
        ),
        nullable=False,
    )
    type = Column(
        postgresql.ENUM(
            "INTERNAL", "EXTERNAL", name="user_type_enum", create_type=False
        ),
        nullable=False,
    )


# Constraints

AbstractEntity.created = relationship(User, foreign_keys=[AbstractEntity.created_by])
AbstractEntity.updated = relationship(User, foreign_keys=[AbstractEntity.updated_by])
Chef.user = relationship(User, foreign_keys=[Chef.user_id])
Client.user = relationship(User, foreign_keys=[Client.user_id])
InventoryIngredient.ingredient = relationship(
    Ingredient, foreign_keys=[InventoryIngredient.ingredient_id]
)
InventoryIngredient.inventory = relationship(
    Inventory, foreign_keys=[InventoryIngredient.inventory_id]
)
Order.chef = relationship(Chef, foreign_keys=[Order.assigned_chef_id])
Order.client = relationship(Client, foreign_keys=[Order.client_id])
OrderDetail.order = relationship(Order, foreign_keys=[OrderDetail.order_id])
OrderDetail.product = relationship(Product, foreign_keys=[OrderDetail.product_id])
OrderStatusHistory.order = relationship(
    Order, foreign_keys=[OrderStatusHistory.order_id]
)
ProductIngredient.product = relationship(
    Product, foreign_keys=[ProductIngredient.product_id]
)
ProductIngredient.ingredient = relationship(
    Ingredient, foreign_keys=[ProductIngredient.ingredient_id]
)

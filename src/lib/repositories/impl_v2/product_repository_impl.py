from datetime import datetime

from src.constants.audit import Status
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import Product
from src.lib.repositories.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self, engine):

        self.engine = engine

    def add(self, product):
        session = create_session(self.engine)
        with session.begin():
            product.created_date = datetime.now()
            product.updated_by = product.created_by
            product.updated_date = product.created_date
            session.add(product)

    def get_by_id(self, product_id):
        session = create_session(self.engine)
        return (
            session.query(Product)
            .filter(Product.id == product_id)
            .filter(Product.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        products = session.query(Product).filter(
            Product.entity_status == Status.ACTIVE.value
        )
        return list(products)

    def delete_by_id(self, product_id, product):
        session = create_session(self.engine)
        with session.begin():
            session.query(Product).filter(Product.id == product_id).update(
                {
                    Product.entity_status: Status.DELETED.value,
                    Product.updated_date: datetime.now(),
                    Product.updated_by: product.updated_by,
                }
            )

    def update_by_id(self, product_id, product):
        session = create_session(self.engine)
        with session.begin():
            product_to_be_updated = (
                session.query(Product).filter(Product.id == product_id).first()
            )
            product_to_be_updated.name = product.name or product_to_be_updated.name
            product_to_be_updated.description = (
                product.description or product_to_be_updated.description
            )
            product_to_be_updated.updated_date = datetime.now()
            product_to_be_updated.updated_by = product.updated_by
            session.add(product_to_be_updated)

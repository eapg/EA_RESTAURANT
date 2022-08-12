from datetime import datetime

from src.constants.audit import Status
from src.core.ioc import get_ioc_instance
from src.lib.entities.sqlalchemy_orm_mapping import Product
from src.lib.repositories_v2.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self):

        ioc = get_ioc_instance()
        self.session = ioc.get_instance("sqlalchemy_session")

    def add(self, product):
        product.created_date = datetime.now()
        product.updated_by = product.created_by
        product.updated_date = product.created_date
        self.session.add(product)
        self.session.commit()

    def get_by_id(self, product_id):
        return (
            self.session.query(Product)
            .filter(Product.id == product_id)
            .filter(Product.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        products = self.session.query(Product).filter(
            Product.entity_status == Status.ACTIVE.value
        )
        return list(products)

    def delete_by_id(self, product_id, product):
        self.session.query(Product).filter(Product.id == product_id).update(
            {
                Product.entity_status: Status.DELETED.value,
                Product.updated_date: datetime.now(),
                Product.updated_by: product.updated_by,
            }
        )
        self.session.commit()

    def update_by_id(self, product_id, product):
        product_to_be_updated = (
            self.session.query(Product).filter(Product.id == product_id).first()
        )
        product_to_be_updated.name = product.name or product_to_be_updated.name
        product_to_be_updated.description = (
            product.description or product_to_be_updated.description
        )
        product_to_be_updated.updated_date = datetime.now()
        product_to_be_updated.updated_by = product.updated_by
        self.session.add(product_to_be_updated)
        self.session.commit()
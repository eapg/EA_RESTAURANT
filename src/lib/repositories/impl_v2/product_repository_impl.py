from datetime import datetime

from src.constants import audit
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, product):
        with self.session.begin():
            product.created_date = datetime.now()
            product.updated_by = product.created_by
            product.updated_date = product.created_date
            self.session.add(product)

    def get_by_id(self, product_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.Product)
            .filter(sqlalchemy_orm_mapping.Product.id == product_id)
            .filter(
                sqlalchemy_orm_mapping.Product.entity_status
                == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        products = self.session.query(sqlalchemy_orm_mapping.Product).filter(
            sqlalchemy_orm_mapping.Product.entity_status == audit.Status.ACTIVE.value
        )
        return list(products)

    def delete_by_id(self, product_id, product):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.Product).filter(
                sqlalchemy_orm_mapping.Product.id == product_id
            ).update(
                {
                    sqlalchemy_orm_mapping.Product.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.Product.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.Product.updated_by: product.updated_by,
                }
            )

    def update_by_id(self, product_id, product):
        with self.session.begin():
            product_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.Product)
                .filter(sqlalchemy_orm_mapping.Product.id == product_id)
                .first()
            )
            product_to_be_updated.name = product.name or product_to_be_updated.name
            product_to_be_updated.description = (
                product.description or product_to_be_updated.description
            )
            product_to_be_updated.updated_date = datetime.now()
            product_to_be_updated.updated_by = product.updated_by
            self.session.add(product_to_be_updated)

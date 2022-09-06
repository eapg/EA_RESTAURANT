from datetime import datetime

from src.constants import audit
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import product_ingredient_repository


class ProductIngredientRepositoryImpl(
    product_ingredient_repository.ProductIngredientRepository
):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, product_ingredient):
        with self.session.begin():
            product_ingredient.created_date = datetime.now()
            product_ingredient.updated_by = product_ingredient.created_by
            product_ingredient.updated_date = product_ingredient.created_date
            self.session.add(product_ingredient)

    def get_by_id(self, product_ingredient_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.ProductIngredient)
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.id == product_ingredient_id
            )
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        product_ingredients = self.session.query(
            sqlalchemy_orm_mapping.ProductIngredient
        ).filter(
            sqlalchemy_orm_mapping.ProductIngredient.entity_status
            == audit.Status.ACTIVE.value
        )
        return list(product_ingredients)

    def delete_by_id(self, product_ingredient_id, product_ingredient):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.ProductIngredient).filter(
                sqlalchemy_orm_mapping.ProductIngredient.id == product_ingredient_id
            ).update(
                {
                    sqlalchemy_orm_mapping.ProductIngredient.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.ProductIngredient.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.ProductIngredient.updated_by: product_ingredient.updated_by,
                }
            )

    def update_by_id(self, product_ingredient_id, product_ingredient):
        with self.session.begin():
            product_ingredient_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.ProductIngredient)
                .filter(
                    sqlalchemy_orm_mapping.ProductIngredient.id == product_ingredient_id
                )
                .first()
            )
            product_ingredient_to_be_updated.user_id = (
                product_ingredient.user_id or product_ingredient_to_be_updated.user_id
            )
            product_ingredient_to_be_updated.skill = (
                product_ingredient.skill or product_ingredient_to_be_updated.skill
            )
            product_ingredient_to_be_updated.updated_date = datetime.now()
            product_ingredient_to_be_updated.updated_by = product_ingredient.updated_by
            self.session.add(product_ingredient_to_be_updated)

    def get_by_product_id(self, product_id):
        product_ingredients = (
            self.session.query(sqlalchemy_orm_mapping.ProductIngredient)
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .filter(sqlalchemy_orm_mapping.ProductIngredient.product_id == product_id)
        )
        return list(product_ingredients)

    def get_product_ingredients_by_product_ids(self, product_ids):
        pass

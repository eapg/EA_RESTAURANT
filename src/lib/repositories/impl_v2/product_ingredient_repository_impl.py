from datetime import datetime

from src.constants.audit import Status
from src.lib.entities.sqlalchemy_orm_mapping import ProductIngredient
from src.lib.repositories.product_ingredient_repository import (
    ProductIngredientRepository,
)


class ProductIngredientRepositoryImpl(ProductIngredientRepository):
    def __init__(self, session):

        self.session = session

    def add(self, product_ingredient):
        with self.session.begin():
            product_ingredient.created_date = datetime.now()
            product_ingredient.updated_by = product_ingredient.created_by
            product_ingredient.updated_date = product_ingredient.created_date
            self.session.add(product_ingredient)

    def get_by_id(self, product_ingredient_id):
        return (
            self.session.query(ProductIngredient)
            .filter(ProductIngredient.id == product_ingredient_id)
            .filter(ProductIngredient.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        product_ingredients = self.session.query(ProductIngredient).filter(
            ProductIngredient.entity_status == Status.ACTIVE.value
        )
        return list(product_ingredients)

    def delete_by_id(self, product_ingredient_id, product_ingredient):
        with self.session.begin():
            self.session.query(ProductIngredient).filter(
                ProductIngredient.id == product_ingredient_id
            ).update(
                {
                    ProductIngredient.entity_status: Status.DELETED.value,
                    ProductIngredient.updated_date: datetime.now(),
                    ProductIngredient.updated_by: product_ingredient.updated_by,
                }
            )

    def update_by_id(self, product_ingredient_id, product_ingredient):
        with self.session.begin():
            product_ingredient_to_be_updated = (
                self.session.query(ProductIngredient)
                .filter(ProductIngredient.id == product_ingredient_id)
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
            self.session.query(ProductIngredient)
            .filter(ProductIngredient.entity_status == Status.ACTIVE.value)
            .filter(ProductIngredient.product_id == product_id)
        )
        return list(product_ingredients)

    def get_product_ingredients_by_product_ids(self, product_ids):
        pass

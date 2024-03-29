from datetime import datetime

from injector import inject
from sqlalchemy.engine.base import Engine

from src.constants.audit import Status
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import ProductIngredient
from src.lib.repositories.product_ingredient_repository import (
    ProductIngredientRepository,
)


class ProductIngredientRepositoryImpl(ProductIngredientRepository):
    @inject
    def __init__(self, engine: Engine):

        self.engine = engine

    def add(self, product_ingredient):
        session = create_session(self.engine)
        with session.begin():
            product_ingredient.entity_status = Status.ACTIVE.value
            product_ingredient.created_date = datetime.now()
            product_ingredient.updated_by = product_ingredient.created_by
            product_ingredient.updated_date = product_ingredient.created_date
            session.add(product_ingredient)
            session.flush()
            session.refresh(product_ingredient)
            return product_ingredient

    def get_by_id(self, product_ingredient_id):
        session = create_session(self.engine)
        return (
            session.query(ProductIngredient)
            .filter(ProductIngredient.entity_status == Status.ACTIVE.value)
            .filter(ProductIngredient.id == product_ingredient_id)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        product_ingredients = session.query(ProductIngredient).filter(
            ProductIngredient.entity_status == Status.ACTIVE.value
        )
        return list(product_ingredients)

    def delete_by_id(self, product_ingredient_id, product_ingredient):
        session = create_session(self.engine)
        with session.begin():
            session.query(ProductIngredient).filter(
                ProductIngredient.id == product_ingredient_id
            ).update(
                {
                    ProductIngredient.entity_status: Status.DELETED.value,
                    ProductIngredient.updated_date: datetime.now(),
                    ProductIngredient.updated_by: product_ingredient.updated_by,
                }
            )

    def update_by_id(self, product_ingredient_id, product_ingredient):
        session = create_session(self.engine)
        with session.begin():
            product_ingredient_to_be_updated = (
                session.query(ProductIngredient)
                .filter(ProductIngredient.id == product_ingredient_id)
                .first()
            )
            product_ingredient_to_be_updated.product_id = (
                product_ingredient.product_id
                or product_ingredient_to_be_updated.product_id
            )
            product_ingredient_to_be_updated.ingredient_id = (
                product_ingredient.ingredient_id
                or product_ingredient_to_be_updated.ingredient_id
            )
            product_ingredient_to_be_updated.quantity = (
                product_ingredient.quantity or product_ingredient_to_be_updated.quantity
            )
            product_ingredient_to_be_updated.cooking_type = (
                product_ingredient.cooking_type
                or product_ingredient_to_be_updated.cooking_type
            )
            product_ingredient_to_be_updated.updated_date = datetime.now()
            product_ingredient_to_be_updated.updated_by = product_ingredient.updated_by
            session.add(product_ingredient_to_be_updated)

    def get_by_product_id(self, product_id):
        session = create_session(self.engine)
        product_ingredients = (
            session.query(ProductIngredient)
            .filter(ProductIngredient.entity_status == Status.ACTIVE.value)
            .filter(ProductIngredient.product_id == product_id)
        )
        return list(product_ingredients)

    def get_product_ingredients_by_product_ids(self, product_ids):
        pass

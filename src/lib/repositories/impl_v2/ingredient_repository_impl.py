from datetime import datetime

from src.constants.audit import Status
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import Ingredient
from src.lib.repositories.ingredient_repository import IngredientRepository


class IngredientRepositoryImpl(IngredientRepository):
    def __init__(self, engine):

        self.engine = engine

    def add(self, ingredient):
        session = create_session(self.engine)
        with session.begin():
            ingredient.created_date = datetime.now()
            ingredient.updated_by = ingredient.created_by
            ingredient.updated_date = ingredient.created_date
            session.add(ingredient)

    def get_by_id(self, ingredient_id):
        session = create_session(self.engine)
        return (
            session.query(Ingredient)
            .filter(Ingredient.id == ingredient_id)
            .filter(Ingredient.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        ingredients = session.query(Ingredient).filter(
            Ingredient.entity_status == Status.ACTIVE.value
        )
        return list(ingredients)

    def delete_by_id(self, ingredient_id, ingredient):
        session = create_session(self.engine)
        with session.begin():
            session.query(Ingredient).filter(Ingredient.id == ingredient_id).update(
                {
                    Ingredient.entity_status: Status.DELETED.value,
                    Ingredient.updated_date: datetime.now(),
                    Ingredient.updated_by: ingredient.updated_by,
                }
            )

    def update_by_id(self, ingredient_id, ingredient):
        session = create_session(self.engine)
        with session.begin():
            ingredient_to_be_updated = (
                session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
            )
            ingredient_to_be_updated.user_id = (
                ingredient.user_id or ingredient_to_be_updated.user_id
            )
            ingredient_to_be_updated.skill = (
                ingredient.skill or ingredient_to_be_updated.skill
            )
            ingredient_to_be_updated.updated_date = datetime.now()
            ingredient_to_be_updated.updated_by = ingredient.updated_by
            session.add(ingredient_to_be_updated)

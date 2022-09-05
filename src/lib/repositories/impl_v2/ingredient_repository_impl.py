from datetime import datetime
from src.constants.audit import Status
from src.core.ioc import get_ioc_instance
from src.lib.entities.sqlalchemy_orm_mapping import Ingredient
from src.lib.repositories.ingredient_repository import IngredientRepository


class IngredientRepositoryImpl(IngredientRepository):
    def __init__(self):

        ioc = get_ioc_instance()
        self.session = ioc.get_instance("sqlalchemy_session")

    def add(self, ingredient):
        with self.session.begin():
            ingredient.created_date = datetime.now()
            ingredient.updated_by = ingredient.created_by
            ingredient.updated_date = ingredient.created_date
            self.session.add(ingredient)

    def get_by_id(self, ingredient_id):
        return (
            self.session.query(Ingredient)
            .filter(Ingredient.id == ingredient_id)
            .filter(Ingredient.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        ingredients = self.session.query(Ingredient).filter(
            Ingredient.entity_status == Status.ACTIVE.value
        )
        return list(ingredients)

    def delete_by_id(self, ingredient_id, ingredient):
        with self.session.begin():
            self.session.query(Ingredient).filter(
                Ingredient.id == ingredient_id
            ).update(
                {
                    Ingredient.entity_status: Status.DELETED.value,
                    Ingredient.updated_date: datetime.now(),
                    Ingredient.updated_by: ingredient.updated_by,
                }
            )

    def update_by_id(self, ingredient_id, ingredient):
        with self.session.begin():
            ingredient_to_be_updated = (
                self.session.query(Ingredient)
                .filter(Ingredient.id == ingredient_id)
                .first()
            )
            ingredient_to_be_updated.user_id = (
                ingredient.user_id or ingredient_to_be_updated.user_id
            )
            ingredient_to_be_updated.skill = (
                ingredient.skill or ingredient_to_be_updated.skill
            )
            ingredient_to_be_updated.updated_date = datetime.now()
            ingredient_to_be_updated.updated_by = ingredient.updated_by
            self.session.add(ingredient_to_be_updated)

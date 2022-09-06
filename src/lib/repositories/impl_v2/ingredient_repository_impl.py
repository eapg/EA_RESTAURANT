from datetime import datetime
from src.constants import audit
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import ingredient_repository


class IngredientRepositoryImpl(ingredient_repository.IngredientRepository):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, ingredient):
        with self.session.begin():
            ingredient.created_date = datetime.now()
            ingredient.updated_by = ingredient.created_by
            ingredient.updated_date = ingredient.created_date
            self.session.add(ingredient)

    def get_by_id(self, ingredient_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.Ingredient)
            .filter(sqlalchemy_orm_mapping.Ingredient.id == ingredient_id)
            .filter(
                sqlalchemy_orm_mapping.Ingredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        ingredients = self.session.query(sqlalchemy_orm_mapping.Ingredient).filter(
            sqlalchemy_orm_mapping.Ingredient.entity_status == audit.Status.ACTIVE.value
        )
        return list(ingredients)

    def delete_by_id(self, ingredient_id, ingredient):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.Ingredient).filter(
                sqlalchemy_orm_mapping.Ingredient.id == ingredient_id
            ).update(
                {
                    sqlalchemy_orm_mapping.Ingredient.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.Ingredient.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.Ingredient.updated_by: ingredient.updated_by,
                }
            )

    def update_by_id(self, ingredient_id, ingredient):
        with self.session.begin():
            ingredient_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.Ingredient)
                .filter(sqlalchemy_orm_mapping.Ingredient.id == ingredient_id)
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

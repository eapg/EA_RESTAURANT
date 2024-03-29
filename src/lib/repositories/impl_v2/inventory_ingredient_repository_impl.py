from datetime import datetime

from injector import inject
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql import func

from src.constants.audit import Status
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import (
    InventoryIngredient,
    ProductIngredient,
)
from src.lib.repositories.inventory_ingredient_repository import (
    InventoryIngredientRepository,
)


class InventoryIngredientRepositoryImpl(InventoryIngredientRepository):
    @inject
    def __init__(self, engine: Engine):

        self.engine = engine

    def add(self, inventory_ingredient):
        session = create_session(self.engine)
        with session.begin():
            inventory_ingredient.entity_status = Status.ACTIVE.value
            inventory_ingredient.created_date = datetime.now()
            inventory_ingredient.updated_by = inventory_ingredient.created_by
            inventory_ingredient.updated_date = inventory_ingredient.created_date
            session.add(inventory_ingredient)
            session.flush()
            session.refresh(inventory_ingredient)
            return inventory_ingredient

    def get_by_id(self, inventory_ingredient_id):
        session = create_session(self.engine)
        return (
            session.query(InventoryIngredient)
            .filter(InventoryIngredient.entity_status == Status.ACTIVE.value)
            .filter(InventoryIngredient.id == inventory_ingredient_id)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        inventory_ingredients = session.query(InventoryIngredient).filter(
            InventoryIngredient.entity_status == Status.ACTIVE.value
        )
        return list(inventory_ingredients)

    def delete_by_id(self, inventory_ingredient_id, inventory_ingredient):
        session = create_session(self.engine)
        with session.begin():
            session.query(InventoryIngredient).filter(
                InventoryIngredient.id == inventory_ingredient_id
            ).update(
                {
                    InventoryIngredient.entity_status: Status.DELETED.value,
                    InventoryIngredient.updated_date: datetime.now(),
                    InventoryIngredient.updated_by: inventory_ingredient.updated_by,
                }
            )

    def update_by_id(self, inventory_ingredient_id, inventory_ingredient):
        session = create_session(self.engine)
        with session.begin():
            inventory_ingredient_to_be_updated = (
                session.query(InventoryIngredient)
                .filter(InventoryIngredient.id == inventory_ingredient_id)
                .first()
            )
            inventory_ingredient_to_be_updated.inventory_id = (
                inventory_ingredient.inventory_id
                or inventory_ingredient_to_be_updated.inventory_id
            )
            inventory_ingredient_to_be_updated.ingredient_id = (
                inventory_ingredient.ingredient_id
                or inventory_ingredient_to_be_updated.ingredient_id
            )
            inventory_ingredient_to_be_updated.quantity = (
                inventory_ingredient.quantity
                or inventory_ingredient_to_be_updated.quantity
            )

            inventory_ingredient_to_be_updated.updated_date = datetime.now()
            inventory_ingredient_to_be_updated.updated_by = (
                inventory_ingredient.updated_by
            )
            session.add(inventory_ingredient_to_be_updated)

    def get_by_ingredient_id(self, ingredient_id):
        session = create_session(self.engine)
        inventory_ingredients = (
            session.query(InventoryIngredient)
            .filter(InventoryIngredient.entity_status == Status.ACTIVE.value)
            .filter(InventoryIngredient.ingredient_id == ingredient_id)
        )
        return list(inventory_ingredients)

    def get_final_product_qty_by_product_ids(self, product_ids):
        session = create_session(self.engine)
        final_product_qty_by_product_ids_query_result = (
            session.query(
                ProductIngredient.product_id,
                func.min(InventoryIngredient.quantity / ProductIngredient.quantity),
            )
            .filter(
                ProductIngredient.ingredient_id == InventoryIngredient.ingredient_id
            )
            .filter(ProductIngredient.product_id.in_(product_ids))
            .filter(ProductIngredient.entity_status == Status.ACTIVE.value)
            .filter(InventoryIngredient.entity_status == Status.ACTIVE.value)
            .group_by(ProductIngredient.product_id)
            .all()
        )

        return dict(
            (product_id, result)
            for product_id, result in final_product_qty_by_product_ids_query_result
        )

    def validate_ingredient_availability(
        self, inventory_id, ingredient_id, quantity_to_use
    ):
        pass

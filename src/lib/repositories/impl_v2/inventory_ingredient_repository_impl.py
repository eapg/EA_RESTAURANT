from datetime import datetime
from sqlalchemy import sql
from src.constants import audit
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import inventory_ingredient_repository


class InventoryIngredientRepositoryImpl(
    inventory_ingredient_repository.InventoryIngredientRepository
):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, inventory_ingredient):
        with self.session.begin():
            inventory_ingredient.created_date = datetime.now()
            inventory_ingredient.updated_by = inventory_ingredient.created_by
            inventory_ingredient.updated_date = inventory_ingredient.created_date
            self.session.add(inventory_ingredient)

    def get_by_id(self, inventory_ingredient_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.InventoryIngredient)
            .filter(
                sqlalchemy_orm_mapping.InventoryIngredient.id == inventory_ingredient_id
            )
            .filter(
                sqlalchemy_orm_mapping.InventoryIngredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        inventory_ingredients = self.session.query(
            sqlalchemy_orm_mapping.InventoryIngredient
        ).filter(
            sqlalchemy_orm_mapping.InventoryIngredient.entity_status
            == audit.Status.ACTIVE.value
        )
        return list(inventory_ingredients)

    def delete_by_id(self, inventory_ingredient_id, inventory_ingredient):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.InventoryIngredient).filter(
                sqlalchemy_orm_mapping.InventoryIngredient.id == inventory_ingredient_id
            ).update(
                {
                    sqlalchemy_orm_mapping.InventoryIngredient.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.InventoryIngredient.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.InventoryIngredient.updated_by: inventory_ingredient.updated_by,
                }
            )

    def update_by_id(self, inventory_ingredient_id, inventory_ingredient):
        with self.session.begin():
            inventory_ingredient_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.InventoryIngredient)
                .filter(
                    sqlalchemy_orm_mapping.InventoryIngredient.id
                    == inventory_ingredient_id
                )
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
            self.session.add(inventory_ingredient_to_be_updated)

    def get_by_ingredient_id(self, ingredient_id):
        inventory_ingredients = (
            self.session.query(sqlalchemy_orm_mapping.InventoryIngredient)
            .filter(
                sqlalchemy_orm_mapping.InventoryIngredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .filter(
                sqlalchemy_orm_mapping.InventoryIngredient.ingredient_id
                == ingredient_id
            )
        )
        return list(inventory_ingredients)

    def get_final_product_qty_by_product_ids(self, product_ids):

        final_product_qty_by_product_ids_query_result = (
            self.session.query(
                sqlalchemy_orm_mapping.ProductIngredient.product_id,
                sql.func.min(
                    sqlalchemy_orm_mapping.InventoryIngredient.quantity
                    / sqlalchemy_orm_mapping.ProductIngredient.quantity
                ),
            )
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.ingredient_id
                == sqlalchemy_orm_mapping.InventoryIngredient.ingredient_id
            )
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.product_id.in_(product_ids)
            )
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .filter(
                sqlalchemy_orm_mapping.InventoryIngredient.entity_status
                == audit.Status.ACTIVE.value
            )
            .group_by(sqlalchemy_orm_mapping.ProductIngredient.product_id)
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

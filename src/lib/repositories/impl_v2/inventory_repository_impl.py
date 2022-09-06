from datetime import datetime
from src.constants import audit
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import inventory_repository


class InventoryRepositoryImpl(inventory_repository.InventoryRepository):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, inventory):
        with self.session.begin():
            inventory.created_date = datetime.now()
            inventory.updated_by = inventory.created_by
            inventory.updated_date = inventory.created_date
            self.session.add(inventory)

    def get_by_id(self, inventory_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.Inventory)
            .filter(sqlalchemy_orm_mapping.Inventory.id == inventory_id)
            .filter(
                sqlalchemy_orm_mapping.Inventory.entity_status
                == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        inventories = self.session.query(sqlalchemy_orm_mapping.Inventory).filter(
            sqlalchemy_orm_mapping.Inventory.entity_status == audit.Status.ACTIVE.value
        )
        return list(inventories)

    def delete_by_id(self, inventory_id, inventory):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.Inventory).filter(
                sqlalchemy_orm_mapping.Inventory.id == inventory_id
            ).update(
                {
                    sqlalchemy_orm_mapping.Inventory.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.Inventory.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.Inventory.updated_by: inventory.updated_by,
                }
            )

    def update_by_id(self, inventory_id, inventory):
        with self.session.begin():
            inventory_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.Inventory)
                .filter(sqlalchemy_orm_mapping.Inventory.id == inventory_id)
                .first()
            )
            inventory_to_be_updated.user_id = (
                inventory.user_id or inventory_to_be_updated.user_id
            )
            inventory_to_be_updated.skill = (
                inventory.skill or inventory_to_be_updated.skill
            )
            inventory_to_be_updated.updated_date = datetime.now()
            inventory_to_be_updated.updated_by = inventory.updated_by
            self.session.add(inventory_to_be_updated)

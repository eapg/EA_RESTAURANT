from datetime import datetime
from src.constants.audit import Status
from src.core.ioc import get_ioc_instance
from src.lib.entities.sqlalchemy_orm_mapping import Inventory
from src.lib.repositories.inventory_repository import InventoryRepository


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self):

        ioc = get_ioc_instance()
        self.session = ioc.get_instance("sqlalchemy_session")

    def add(self, inventory):
        with self.session.begin():
            inventory.created_date = datetime.now()
            inventory.updated_by = inventory.created_by
            inventory.updated_date = inventory.created_date
            self.session.add(inventory)

    def get_by_id(self, inventory_id):
        return (
            self.session.query(Inventory)
            .filter(Inventory.id == inventory_id)
            .filter(Inventory.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        inventories = self.session.query(Inventory).filter(
            Inventory.entity_status == Status.ACTIVE.value
        )
        return list(inventories)

    def delete_by_id(self, inventory_id, inventory):
        with self.session.begin():
            self.session.query(Inventory).filter(Inventory.id == inventory_id).update(
                {
                    Inventory.entity_status: Status.DELETED.value,
                    Inventory.updated_date: datetime.now(),
                    Inventory.updated_by: inventory.updated_by,
                }
            )

    def update_by_id(self, inventory_id, inventory):
        with self.session.begin():
            inventory_to_be_updated = (
                self.session.query(Inventory)
                .filter(Inventory.id == inventory_id)
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

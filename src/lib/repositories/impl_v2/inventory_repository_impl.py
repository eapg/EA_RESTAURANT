from datetime import datetime

from src.constants.audit import Status
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import Inventory
from src.lib.repositories.inventory_repository import InventoryRepository


class InventoryRepositoryImpl(InventoryRepository):
    def __init__(self, engine):

        self.engine = engine

    def add(self, inventory):
        session = create_session(self.engine)
        with session.begin():
            inventory.created_date = datetime.now()
            inventory.updated_by = inventory.created_by
            inventory.updated_date = inventory.created_date
            session.add(inventory)

    def get_by_id(self, inventory_id):
        session = create_session(self.engine)
        return (
            session.query(Inventory)
            .filter(Inventory.id == inventory_id)
            .filter(Inventory.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        inventories = session.query(Inventory).filter(
            Inventory.entity_status == Status.ACTIVE.value
        )
        return list(inventories)

    def delete_by_id(self, inventory_id, inventory):
        session = create_session(self.engine)
        with session.begin():
            session.query(Inventory).filter(Inventory.id == inventory_id).update(
                {
                    Inventory.entity_status: Status.DELETED.value,
                    Inventory.updated_date: datetime.now(),
                    Inventory.updated_by: inventory.updated_by,
                }
            )

    def update_by_id(self, inventory_id, inventory):
        session = create_session(self.engine)
        with session.begin():
            inventory_to_be_updated = (
                session.query(Inventory).filter(Inventory.id == inventory_id).first()
            )
            inventory_to_be_updated.user_id = (
                inventory.user_id or inventory_to_be_updated.user_id
            )
            inventory_to_be_updated.skill = (
                inventory.skill or inventory_to_be_updated.skill
            )
            inventory_to_be_updated.updated_date = datetime.now()
            inventory_to_be_updated.updated_by = inventory.updated_by
            session.add(inventory_to_be_updated)

from datetime import datetime
from sqlalchemy import not_
from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.core.ioc import get_ioc_instance
from src.lib.entities.sqlalchemy_orm_mapping import Chef, Order
from src.lib.repositories_v2.chef_repository import ChefRepository


class ChefRepositoryImpl(ChefRepository):
    def __init__(self):

        ioc = get_ioc_instance()
        self.session = ioc.get_instance("sqlalchemy_session")

    def add(self, chef):
        chef.created_date = datetime.now()
        chef.updated_by = chef.created_by
        chef.updated_date = chef.created_date
        self.session.add(chef)
        self.session.commit()

    def get_by_id(self, chef_id):
        return (
            self.session.query(Chef)
            .filter(Chef.id == chef_id)
            .filter(Chef.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        chefs = self.session.query(Chef).filter(
            Chef.entity_status == Status.ACTIVE.value
        )
        return list(chefs)

    def delete_by_id(self, chef_id, chef):
        self.session.query(Chef).filter(Chef.id == chef_id).update(
            {
                Chef.entity_status: Status.DELETED.value,
                Chef.updated_date: datetime.now(),
                Chef.updated_by: chef.updated_by,
            }
        )
        self.session.commit()

    def update_by_id(self, chef_id, chef):
        chef_to_be_updated = self.session.query(Chef).filter(Chef.id == chef_id).first()
        chef_to_be_updated.user_id = chef.user_id or chef_to_be_updated.user_id
        chef_to_be_updated.skill = chef.skill or chef_to_be_updated.skill
        chef_to_be_updated.updated_date = datetime.now()
        chef_to_be_updated.updated_by = chef.updated_by
        self.session.add(chef_to_be_updated)
        self.session.commit()

    def get_available_chefs(self):

        available_chef_ids = (
            self.session.query(Chef.id)
            .filter(Chef.entity_status == Status.ACTIVE.value)
            .filter(
                not_(
                    self.session.query(Order.assigned_chef_id)
                    .filter(Order.entity_status == Status.ACTIVE.value)
                    .filter(Order.assigned_chef_id == Chef.id)
                    .filter(Order.status == OrderStatus.IN_PROCESS.name)
                    .exists()
                )
            )
        )

        return [chef_id[0] for chef_id in available_chef_ids]

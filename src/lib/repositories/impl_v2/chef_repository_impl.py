from datetime import datetime

from sqlalchemy import not_

from src.constants.audit import Status
from src.constants.order_status import OrderStatus
from src.core.sqlalchemy_config import create_session
from src.lib.entities.sqlalchemy_orm_mapping import Chef, Order
from src.lib.repositories.chef_repository import ChefRepository


class ChefRepositoryImpl(ChefRepository):
    def __init__(self, engine):

        self.engine = engine

    def add(self, chef):
        session = create_session(self.engine)
        with session.begin():
            chef.created_date = datetime.now()
            chef.updated_by = chef.created_by
            chef.updated_date = chef.created_date
            session.add(chef)

    def get_by_id(self, chef_id):
        session = create_session(self.engine)
        return (
            session.query(Chef)
            .filter(Chef.id == chef_id)
            .filter(Chef.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        session = create_session(self.engine)
        chefs = session.query(Chef).filter(Chef.entity_status == Status.ACTIVE.value)
        return list(chefs)

    def delete_by_id(self, chef_id, chef):
        session = create_session(self.engine)
        with session.begin():
            session.query(Chef).filter(Chef.id == chef_id).update(
                {
                    Chef.entity_status: Status.DELETED.value,
                    Chef.updated_date: datetime.now(),
                    Chef.updated_by: chef.updated_by,
                }
            )

    def update_by_id(self, chef_id, chef):
        session = create_session(self.engine)
        with session.begin():
            chef_to_be_updated = session.query(Chef).filter(Chef.id == chef_id).first()
            chef_to_be_updated.user_id = chef.user_id or chef_to_be_updated.user_id
            chef_to_be_updated.skill = chef.skill or chef_to_be_updated.skill
            chef_to_be_updated.updated_date = datetime.now()
            chef_to_be_updated.updated_by = chef.updated_by
            session.add(chef_to_be_updated)

    def get_available_chefs(self):
        session = create_session(self.engine)
        available_chef_ids = (
            session.query(Chef.id)
            .filter(Chef.entity_status == Status.ACTIVE.value)
            .filter(
                not_(
                    session.query(Order.assigned_chef_id)
                    .filter(Order.entity_status == Status.ACTIVE.value)
                    .filter(Order.assigned_chef_id == Chef.id)
                    .filter(Order.status == OrderStatus.IN_PROCESS.name)
                    .exists()
                )
            )
        )

        return [chef_id[0] for chef_id in available_chef_ids]

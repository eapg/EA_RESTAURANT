from datetime import datetime
import sqlalchemy
from src.constants import audit
from src.constants import order_status
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import chef_repository


class ChefRepositoryImpl(chef_repository.ChefRepository):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, chef):

        with self.session.begin():
            chef.created_date = datetime.now()
            chef.updated_by = chef.created_by
            chef.updated_date = chef.created_date
            self.session.add(chef)

    def get_by_id(self, chef_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.Chef)
            .filter(sqlalchemy_orm_mapping.Chef.id == chef_id)
            .filter(
                sqlalchemy_orm_mapping.Chef.entity_status == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        chefs = self.session.query(sqlalchemy_orm_mapping.Chef).filter(
            sqlalchemy_orm_mapping.Chef.entity_status == audit.Status.ACTIVE.value
        )
        return list(chefs)

    def delete_by_id(self, chef_id, chef):

        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.Chef).filter(
                sqlalchemy_orm_mapping.Chef.id == chef_id
            ).update(
                {
                    sqlalchemy_orm_mapping.Chef.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.Chef.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.Chef.updated_by: chef.updated_by,
                }
            )

    def update_by_id(self, chef_id, chef):

        with self.session.begin():
            chef_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.Chef)
                .filter(sqlalchemy_orm_mapping.Chef.id == chef_id)
                .first()
            )
            chef_to_be_updated.user_id = chef.user_id or chef_to_be_updated.user_id
            chef_to_be_updated.skill = chef.skill or chef_to_be_updated.skill
            chef_to_be_updated.updated_date = datetime.now()
            chef_to_be_updated.updated_by = chef.updated_by
            self.session.add(chef_to_be_updated)

    def get_available_chefs(self):

        available_chef_ids = (
            self.session.query(sqlalchemy_orm_mapping.Chef.id)
            .filter(
                sqlalchemy_orm_mapping.Chef.entity_status == audit.Status.ACTIVE.value
            )
            .filter(
                sqlalchemy.not_(
                    self.session.query(sqlalchemy_orm_mapping.Order.assigned_chef_id)
                    .filter(
                        sqlalchemy_orm_mapping.Order.entity_status
                        == audit.Status.ACTIVE.value
                    )
                    .filter(
                        sqlalchemy_orm_mapping.Order.assigned_chef_id
                        == sqlalchemy_orm_mapping.Chef.id
                    )
                    .filter(
                        sqlalchemy_orm_mapping.Order.status
                        == order_status.OrderStatus.IN_PROCESS.name
                    )
                    .exists()
                )
            )
        )

        return [chef_id[0] for chef_id in available_chef_ids]

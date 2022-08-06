from src.lib.entities.sqlalchemy_orm_mapping import Chef
from src.constants.audit import Status


def build_chef(
    chef_id=None,
    user_id=None,
    name=None,
    skill=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):

    chef = Chef()
    chef.id = chef_id
    chef.user_id = user_id or 1
    chef.name = name or "testing-chef"
    chef.skill = skill or 1
    chef.entity_status = entity_status or Status.ACTIVE.value
    chef.created_by = create_by or 1
    chef.updated_by = update_by or create_by

    return chef


def build_chefs(count=1):
    return [build_chef(name=f"testing-chef{n}", skill=n, chef_id=n) for n in range(count)]

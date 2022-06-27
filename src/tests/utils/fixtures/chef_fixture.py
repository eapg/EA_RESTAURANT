from src.constants.audit import Status
from src.lib.entities.chef import Chef


def build_chef(chef_id=None, name=None, chef_skills=None, entity_status=None):

    chef = Chef()
    chef.id = chef_id
    chef.name = name or "testing-chef"
    chef.chef_skills = chef_skills or "basic"
    chef.entity_status = entity_status or Status.ACTIVE

    return chef


def build_chefs(count=1):
    return [
        build_chef(name=f"testing-chef{n}", chef_skills="testing-chef_skills")
        for n in range(count)
    ]

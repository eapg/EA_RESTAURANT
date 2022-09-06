from src.constants import audit
from src.lib.entities import chef


def build_chef(chef_id=None, name=None, chef_skills=None, entity_status=None):

    chef_instance = chef.Chef()
    chef_instance.id = chef_id
    chef_instance.name = name or "testing-chef"
    chef_instance.chef_skills = chef_skills or "basic"
    chef_instance.entity_status = entity_status or audit.Status.ACTIVE

    return chef_instance


def build_chefs(count=1):
    return [
        build_chef(name=f"testing-chef{n}", chef_skills="testing-chef_skills")
        for n in range(count)
    ]

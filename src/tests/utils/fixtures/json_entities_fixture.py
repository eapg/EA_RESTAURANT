def build_chef(
    chef_id=None, user_id=None, skill=None, created_by=None, updated_by=None
):

    chef = {
        "id": chef_id or 1,
        "user_id": user_id or 1,
        "skill": skill or 5,
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }
    return chef


def build_ingredient(
    ingredient_id=None,
    ingredient_name=None,
    ingredient_description=None,
    created_by=None,
    updated_by=None,
):
    ingredient = {
        "id": ingredient_id or 1,
        "name": ingredient_name or "test ingredient",
        "description": ingredient_description or "test description",
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return ingredient

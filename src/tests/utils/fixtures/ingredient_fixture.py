from src.constants.audit import Status
from src.lib.entities.ingredient import Ingredient


def build_ingredient(
    ingredient_id=None,
    name=None,
    description=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):
    ingredient = Ingredient()
    ingredient.id = ingredient_id
    ingredient.name = name or "testing-ingredient"
    ingredient.description = description or "testing-description"
    ingredient.entity_status = entity_status or Status.ACTIVE
    ingredient.create_by = create_by
    ingredient.update_by = update_by

    return ingredient


def build_ingredients(count=1):
    return [
        build_ingredient(
            name=f"testing-ingredient{n}", description=f"testing-description{n}"
        )
        for n in range(count)
    ]

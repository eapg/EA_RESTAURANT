from src.constants import audit
from src.lib.entities import ingredient


def build_ingredient(
    ingredient_id=None,
    name=None,
    description=None,
    entity_status=None,
    create_by=None,
    update_by=None,
):
    ingredient_instance = ingredient.Ingredient()
    ingredient_instance.id = ingredient_id
    ingredient_instance.name = name or "testing-ingredient"
    ingredient_instance.description = description or "testing-description"
    ingredient_instance.entity_status = entity_status or audit.Status.ACTIVE
    ingredient_instance.create_by = create_by
    ingredient_instance.update_by = update_by

    return ingredient_instance


def build_ingredients(count=1):
    return [
        build_ingredient(
            name=f"testing-ingredient{n}", description=f"testing-description{n}"
        )
        for n in range(count)
    ]

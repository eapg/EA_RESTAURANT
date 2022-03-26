from lib.entities.ingredient import Ingredient


def build_ingredient(ingredient_id=None, name=None, description=None):
    ingredient = Ingredient()
    ingredient.id = ingredient_id
    ingredient.name = name or 'testing-ingredient'
    ingredient.description = description or 'testing-description'

    return ingredient


def build_ingredients(count=1):
    return [build_ingredient(name=f'testing-ingredient{n}', description=f'testing-description{n}') for n in
            range(count)]

# product util to get the sum of ingredients time to know the time a product will last to be ready


def product_preparation_time(product, chef):

    preparation_time = sum(
        [ingredient.ingredient_type.value for ingredient in product.ingredients]
    )
    return preparation_time / chef.chef_skills

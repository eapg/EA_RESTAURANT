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


def build_inventory_ingredient(
    inventory_ingredient_id=None,
    ingredient_id=None,
    inventory_id=None,
    quantity=None,
    created_by=None,
    updated_by=None,
):

    inventory_ingredient = {
        "id": inventory_ingredient_id or 1,
        "ingredient_id": ingredient_id or 1,
        "inventory_id": inventory_id or 1,
        "quantity": quantity or 5,
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return inventory_ingredient


def build_inventory(
    inventory_id=None,
    name=None,
    created_by=None,
    updated_by=None,
):

    inventory = {
        "id": inventory_id or 1,
        "name": name or "inventory 1",
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return inventory


def build_order_detail(
    order_detail_id=None,
    order_id=None,
    product_id=None,
    quantity=None,
    created_by=None,
    updated_by=None,
):

    order_detail = {
        "id": order_detail_id or 1,
        "order_id": order_id or 1,
        "product_id": product_id or 1,
        "quantity": quantity or 10,
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return order_detail

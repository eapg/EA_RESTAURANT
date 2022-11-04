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


def build_order(
    order_id=None,
    status=None,
    assigned_chef_id=None,
    client_id=None,
    created_by=None,
    updated_by=None,
):

    order = {
        "id": order_id or 1,
        "status": status or "NEW_ORDER",
        "assigned_chef_id": assigned_chef_id or 1,
        "client_id": client_id or 1,
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return order


def build_product_ingredient(
    product_ingredient_id=None,
    product_id=None,
    ingredient_id=None,
    quantity=None,
    cooking_type=None,
    created_by=None,
    updated_by=None,
):

    product_ingredient = {
        "id": product_ingredient_id or 1,
        "product_id": product_id or 1,
        "ingredient_id": ingredient_id or 1,
        "quantity": quantity or 5,
        "cooking_type": cooking_type or "ADDING",
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return product_ingredient


def build_product(
    product_id=None,
    name=None,
    description=None,
    created_by=None,
    updated_by=None,
):

    product_ingredient = {
        "id": product_id or 1,
        "name": name or "product 1",
        "description": description or "product 1 description",
        "created_by": created_by or 1,
        "updated_by": updated_by or 1,
    }

    return product_ingredient


def build_order_status_history(
    order_status_history_id=None,
    order_id=None,
    from_time=None,
    to_time=None,
    to_status=None,
    mongo_order_status_history_uuid=None,
    etl_status=None,
    from_status=None,
    updated_by=None,
):

    order_status_history = {
        "id": order_status_history_id or 1,
        "order_id": order_id or 1,
        "from_time": from_time or "2022-11-04T15:59:59.163000",
        "from_status": from_status or "NEW_ORDER",
        "to_time": to_time or "2022-11-04T15:59:59.163000",
        "to_status": to_status or "IN_PROCESS",
        "mongo_order_status_history_uuid": mongo_order_status_history_uuid or "test uuid",
        "etl_status": etl_status or "PROCESSED",
        "created_by": 1,
        "updated_by": updated_by or 1,
    }

    return order_status_history

from datetime import datetime
from sqlalchemy.sql import text
from sqlalchemy import case, func
from src.constants.audit import Status
from src.core.ioc import get_ioc_instance
from src.lib.entities.sqlalchemy_orm_mapping import (
    InventoryIngredient,
    Order,
    OrderDetail,
    ProductIngredient,
)
from src.lib.repositories.order_repository import OrderRepository

sql_query_to_reduce_ingredients_from_inventory = """
                with order_ingredients_cte as (
                      select product_ingredients.id
                        from product_ingredients
                  inner join order_details
                          on product_ingredients.product_id = order_details.product_id
                       where order_details.order_id = :order_id
                )

                update inventory_ingredients as in_table
                    set quantity = in_table.quantity - pro_table.quantity
                   from product_ingredients as pro_table
                  where pro_table.ingredient_id = in_table.ingredient_id and
                        pro_table.id in (select id from order_ingredients_cte)
                """


class OrderRepositoryImpl(OrderRepository):
    def __init__(self):

        ioc = get_ioc_instance()
        self.session = ioc.get_instance("sqlalchemy_session")

    def add(self, order):
        with self.session.begin():
            order.created_date = datetime.now()
            order.updated_by = order.created_by
            order.updated_date = order.created_date
            self.session.add(order)

    def get_by_id(self, order_id):
        return (
            self.session.query(Order)
            .filter(Order.id == order_id)
            .filter(Order.entity_status == Status.ACTIVE.value)
            .first()
        )

    def get_all(self):
        orders = self.session.query(Order).filter(
            Order.entity_status == Status.ACTIVE.value
        )
        return list(orders)

    def delete_by_id(self, order_id, order):
        with self.session.begin():
            self.session.query(Order).filter(Order.id == order_id).update(
                {
                    Order.entity_status: Status.DELETED.value,
                    Order.updated_date: datetime.now(),
                    Order.updated_by: order.updated_by,
                }
            )

    def update_by_id(self, order_id, order):
        with self.session.begin():
            order_to_be_updated = (
                self.session.query(Order).filter(Order.id == order_id).first()
            )
            order_to_be_updated.user_id = order.user_id or order_to_be_updated.user_id
            order_to_be_updated.skill = order.skill or order_to_be_updated.skill
            order_to_be_updated.updated_date = datetime.now()
            order_to_be_updated.updated_by = order.updated_by
            self.session.add(order_to_be_updated)

    def get_orders_by_status(self, order_status, order_limit=None):
        orders_by_status = (
            self.session.query(Order)
            .filter(Order.entity_status == Status.ACTIVE.value)
            .filter(Order.status == order_status)
            .limit(order_limit)
            .all()
        )

        return orders_by_status

    def get_order_ingredients_by_order_id(self, order_id):

        product_ingredients_by_order_id = (
            self.session.query(ProductIngredient)
            .filter(
                ProductIngredient.entity_status == Status.ACTIVE.value,
                OrderDetail.entity_status == Status.ACTIVE.value,
            )
            .join(OrderDetail, ProductIngredient.product_id == OrderDetail.product_id)
            .filter(OrderDetail.order_id == order_id)
        )

        return list(product_ingredients_by_order_id)

    def get_validated_orders_map(self, orders_to_process):

        case_query = case(
            (
                func.min(
                    InventoryIngredient.quantity
                    / ProductIngredient.quantity
                    / OrderDetail.quantity
                )
                > 0,
                True,
            ),
            else_=False,
        )

        validation_orders = (
            self.session.query(OrderDetail.order_id, case_query)
            .join(
                ProductIngredient,
                ProductIngredient.product_id == OrderDetail.product_id,
            )
            .join(
                InventoryIngredient,
                ProductIngredient.ingredient_id == InventoryIngredient.ingredient_id,
            )
            .filter(
                OrderDetail.entity_status == Status.ACTIVE.value,
                ProductIngredient.entity_status == Status.ACTIVE.value,
                InventoryIngredient.entity_status == Status.ACTIVE.value,
                OrderDetail.order_id.in_([order.id for order in orders_to_process]),
            )
            .group_by(OrderDetail.order_id)
            .all()
        )
        validation_order_map = dict(
            (product_id, result) for product_id, result in validation_orders
        )
        return validation_order_map

    def reduce_order_ingredients_from_inventory(self, order_id):
        engine = self.session.get_bind()

        with engine.begin() as conn:

            conn.execute(
                text(sql_query_to_reduce_ingredients_from_inventory),
                {"order_id": order_id},
            )

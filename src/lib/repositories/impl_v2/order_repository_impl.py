from datetime import datetime
from sqlalchemy import sql
import sqlalchemy
from src.constants import audit
from src.core import ioc
from src.lib.entities import sqlalchemy_orm_mapping
from src.lib.repositories import order_repository

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


class OrderRepositoryImpl(order_repository.OrderRepository):
    def __init__(self):

        ioc_instance = ioc.get_ioc_instance()
        self.session = ioc_instance.get_instance("sqlalchemy_session")

    def add(self, order):
        with self.session.begin():
            order.created_date = datetime.now()
            order.updated_by = order.created_by
            order.updated_date = order.created_date
            self.session.add(order)

    def get_by_id(self, order_id):
        return (
            self.session.query(sqlalchemy_orm_mapping.Order)
            .filter(sqlalchemy_orm_mapping.Order.id == order_id)
            .filter(
                sqlalchemy_orm_mapping.Order.entity_status == audit.Status.ACTIVE.value
            )
            .first()
        )

    def get_all(self):
        orders = self.session.query(sqlalchemy_orm_mapping.Order).filter(
            sqlalchemy_orm_mapping.Order.entity_status == audit.Status.ACTIVE.value
        )
        return list(orders)

    def delete_by_id(self, order_id, order):
        with self.session.begin():
            self.session.query(sqlalchemy_orm_mapping.Order).filter(
                sqlalchemy_orm_mapping.Order.id == order_id
            ).update(
                {
                    sqlalchemy_orm_mapping.Order.entity_status: audit.Status.DELETED.value,
                    sqlalchemy_orm_mapping.Order.updated_date: datetime.now(),
                    sqlalchemy_orm_mapping.Order.updated_by: order.updated_by,
                }
            )

    def update_by_id(self, order_id, order):
        with self.session.begin():
            order_to_be_updated = (
                self.session.query(sqlalchemy_orm_mapping.Order)
                .filter(sqlalchemy_orm_mapping.Order.id == order_id)
                .first()
            )
            order_to_be_updated.user_id = order.user_id or order_to_be_updated.user_id
            order_to_be_updated.skill = order.skill or order_to_be_updated.skill
            order_to_be_updated.updated_date = datetime.now()
            order_to_be_updated.updated_by = order.updated_by
            self.session.add(order_to_be_updated)

    def get_orders_by_status(self, order_status, order_limit=None):
        orders_by_status = (
            self.session.query(sqlalchemy_orm_mapping.Order)
            .filter(
                sqlalchemy_orm_mapping.Order.entity_status == audit.Status.ACTIVE.value
            )
            .filter(sqlalchemy_orm_mapping.Order.status == order_status)
            .limit(order_limit)
            .all()
        )

        return orders_by_status

    def get_order_ingredients_by_order_id(self, order_id):

        product_ingredients_by_order_id = (
            self.session.query(sqlalchemy_orm_mapping.ProductIngredient)
            .filter(
                sqlalchemy_orm_mapping.ProductIngredient.entity_status
                == audit.Status.ACTIVE.value,
                sqlalchemy_orm_mapping.OrderDetail.entity_status
                == audit.Status.ACTIVE.value,
            )
            .join(
                sqlalchemy_orm_mapping.OrderDetail,
                sqlalchemy_orm_mapping.ProductIngredient.product_id
                == sqlalchemy_orm_mapping.OrderDetail.product_id,
            )
            .filter(sqlalchemy_orm_mapping.OrderDetail.order_id == order_id)
        )

        return list(product_ingredients_by_order_id)

    def get_validated_orders_map(self, orders_to_process):

        case_query = sqlalchemy.case(
            (
                sqlalchemy.func.min(
                    sqlalchemy_orm_mapping.InventoryIngredient.quantity
                    / sqlalchemy_orm_mapping.ProductIngredient.quantity
                    / sqlalchemy_orm_mapping.OrderDetail.quantity
                )
                > 0,
                True,
            ),
            else_=False,
        )

        validation_orders = (
            self.session.query(sqlalchemy_orm_mapping.OrderDetail.order_id, case_query)
            .join(
                sqlalchemy_orm_mapping.ProductIngredient,
                sqlalchemy_orm_mapping.ProductIngredient.product_id
                == sqlalchemy_orm_mapping.OrderDetail.product_id,
            )
            .join(
                sqlalchemy_orm_mapping.InventoryIngredient,
                sqlalchemy_orm_mapping.ProductIngredient.ingredient_id
                == sqlalchemy_orm_mapping.InventoryIngredient.ingredient_id,
            )
            .filter(
                sqlalchemy_orm_mapping.OrderDetail.entity_status
                == audit.Status.ACTIVE.value,
                sqlalchemy_orm_mapping.ProductIngredient.entity_status
                == audit.Status.ACTIVE.value,
                sqlalchemy_orm_mapping.InventoryIngredient.entity_status
                == audit.Status.ACTIVE.value,
                sqlalchemy_orm_mapping.OrderDetail.order_id.in_(
                    [order.id for order in orders_to_process]
                ),
            )
            .group_by(sqlalchemy_orm_mapping.OrderDetail.order_id)
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
                sql.text(sql_query_to_reduce_ingredients_from_inventory),
                {"order_id": order_id},
            )

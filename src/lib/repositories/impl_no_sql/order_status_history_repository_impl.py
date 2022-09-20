from datetime import datetime

from mongoengine import connect
from pymongo import MongoClient
from src.constants.audit import Status, InternalUsers
from src.lib.entities.mongo_engine_odm_mapping import OrderStatusHistory
from src.lib.repositories.order_status_history_repository import (
    OrderStatusHistoryRepository,
)


class OrderStatusHistoryRepositoryImpl(OrderStatusHistoryRepository):
    def __init__(self, mongo_engine_connection):
        self.mongo_engine_connection = mongo_engine_connection
        self.mongo_client = MongoClient("mongodb://localhost")

    def add(self, order_status_history):
        order_status_history.created_date = datetime.now()
        order_status_history.updated_by = order_status_history.created_by
        order_status_history.updated_date = order_status_history.created_date
        order_status_history.save()

    def get_by_id(self, order_status_history_id):
        order_status_history = OrderStatusHistory.objects.get(
            id=order_status_history_id, entity_status=Status.ACTIVE.value
        )
        return order_status_history

    def get_all(self):
        order_status_histories = OrderStatusHistory.objects(
            entity_status=Status.ACTIVE.value
        )
        return order_status_histories

    def delete_by_id(self, order_status_history_id, order_status_history):
        order_status_history_to_delete = OrderStatusHistory.objects(
            id=order_status_history_id
        ).update_one(
            entity_status=Status.DELETED.value,
            updated_date=datetime.now(),
            updated_by=order_status_history.updated_by,
        )

    def update_by_id(self, order_status_history_id, order_status_history):
        order_status_history_to_update = OrderStatusHistory.objects.get(
            id=order_status_history_id
        )
        order_status_history_to_update.order_id = (
            order_status_history.order_id or order_status_history_to_update.order_id
        )
        order_status_history_to_update.from_time = (
            order_status_history.from_time or order_status_history_to_update.from_time
        )
        order_status_history_to_update.to_time = (
            order_status_history.to_time or order_status_history_to_update.to_time
        )
        order_status_history_to_update.from_status = (
            order_status_history.from_time or order_status_history_to_update.from_status
        )
        order_status_history_to_update.to_status = (
            order_status_history.to_status or order_status_history_to_update.to_status
        )
        order_status_history_to_update.updated_date = datetime.now()
        order_status_history_to_update.updated_by = order_status_history.updated_by
        order_status_history_to_update.save()

    def get_by_order_id(self, order_id):
        order_status_history = OrderStatusHistory.objects(
            order_id=order_id, entity_status=Status.ACTIVE.value
        )
        return order_status_history

    def get_last_status_history_by_order_id(self, order_id):

        try:
            last_order_status_history = (
                OrderStatusHistory.objects(order_id=order_id)
                .order_by("-from_time")
                .limit(1)
            )
            return last_order_status_history[0]

        except IndexError:
            return None

    def set_next_status_history_by_order_id(self, order_id, new_status):

        last_order_status_history = self.get_last_status_history_by_order_id(order_id)

        if last_order_status_history:

            last_order_status_history.to_status = new_status
            last_order_status_history.to_time = datetime.now()
            last_order_status_history.save()

        new_status_history = OrderStatusHistory()
        new_status_history.from_status = new_status
        new_status_history.from_time = datetime.now()
        new_status_history.entity_status = Status.ACTIVE.value
        new_status_history.order_id = order_id
        new_status_history.created_by = InternalUsers.KITCHEN_SIMULATOR.value
        new_status_history.updated_by = new_status_history.created_by
        new_status_history.save()

    def update_batch_processed(self, order_status_history_ids):

        db = self.mongo_client["ea_restaurant"]
        collection = db["order_status_histories"]
        collection.update_many(
            {"_id": {"$in": order_status_history_ids}},
            {"$set": {"etl_status": "PROCESSED"}},
        )

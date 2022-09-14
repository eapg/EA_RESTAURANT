from mongoengine import Document, IntField, DateTimeField, StringField


class BaseEntity(Document):
    entity_status = StringField()
    created_date = DateTimeField()
    updated_date = DateTimeField()
    created_by = IntField()
    updated_by = IntField()

    meta = {"allow_inheritance": True, "abstract": True}


class OrderStatusHistory(BaseEntity):

    postgresql_order_status_history_id = IntField()
    order_id = IntField(required=True)
    from_time = DateTimeField()
    to_time = DateTimeField()
    from_status = StringField()
    to_status = StringField()

    meta = {"collection": "order_status_histories"}

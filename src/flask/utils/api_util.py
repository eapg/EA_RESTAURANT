def fetch_class_from_data(entity, data):

    for key in data:
        setattr(entity, key, data.get(key))

    return entity

# structure for the singleton decorator


def singleton(cls):

    instance = {}

    def wrapper(*args, **kwargs):
        if cls not in instance:
            instance[cls.__name__] = cls(*args, **kwargs)
        return instance[cls.__name__]

    return wrapper

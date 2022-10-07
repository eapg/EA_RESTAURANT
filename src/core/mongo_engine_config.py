from mongoengine import connect


def mongo_engine_connection():

    conn = connect(db="ea_restaurant", host="localhost", port=27017)
    return conn

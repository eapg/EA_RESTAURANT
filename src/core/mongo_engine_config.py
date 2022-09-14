from mongoengine import connect


def mongo_engine_connexion():

    connect(db="ea_restaurant", host="localhost", port=27017)

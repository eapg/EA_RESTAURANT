# ORM sqlalchemy configuration file

import sqlalchemy
from sqlalchemy import orm


def create_session():
    engine = sqlalchemy.create_engine("postgresql://postgres:1234@localhost/ea_restaurant")
    session_creation = orm.sessionmaker(engine)
    session = session_creation()
    return session

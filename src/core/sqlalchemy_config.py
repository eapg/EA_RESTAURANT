# ORM sqlalchemy session creation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    return create_engine("postgresql://postgres:1234@localhost/ea_restaurant")


def create_session(engine: object):
    session_creation = sessionmaker(
        bind=engine, expire_on_commit=False, autocommit=True
    )
    session = session_creation()
    return session

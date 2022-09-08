# ORM sqlalchemy configuration file

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():
    engine = create_engine("postgresql://postgres:1234@localhost/ea_restaurant")
    session_creation = sessionmaker(bind=engine, expire_on_commit=False, autocommit=True)
    session = session_creation()
    return session

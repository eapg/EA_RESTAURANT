# ORM sqlalchemy session creation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.env_config import get_env_config_instance


def get_engine():
    env_config = get_env_config_instance()
    return create_engine(env_config.get_postgres_db_uri())


def create_session(engine: object):
    session_creation = sessionmaker(
        bind=engine, expire_on_commit=False, autocommit=True
    )
    session = session_creation()
    return session

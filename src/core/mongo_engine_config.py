from mongoengine import connect

from src.env_config import get_env_config_instance


def mongo_engine_connection():
    env_config = get_env_config_instance()
    conn = connect(
        db=env_config.mongo_db_name,
        host=env_config.mongo_host,
        port=env_config.mongo_port,
    )
    return conn

import os

from dotenv import load_dotenv

dir_name = os.path.dirname(__file__)
env_path = os.path.join(dir_name, "..", ".env")
load_dotenv(dotenv_path=env_path)

current_env = os.environ.get("ENV", "local")
current_env_path = os.path.join(dir_name, "..", f".env.{current_env}")
load_dotenv(dotenv_path=current_env_path)


def get_postgres_db_uri(
    postgres_user, postgres_password, postgres_host, postgres_db_name
):
    return f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db_name}"


# pylint: disable=R0902
class EnvConfig:
    def __init__(self):
        # postgresql config
        self.postgres_host = os.environ.get("POSTGRESQL_HOST")
        self.postgres_user = os.environ.get("POSTGRESQL_USER")
        self.postgres_password = os.environ.get("POSTGRESQL_PASSWORD")
        self.postgres_db_name = os.environ.get("POSTGRESQL_DB_NAME")

        # mongo config
        self.mongo_host = os.environ.get("MONGO_HOST")
        self.mongo_port = int(os.environ.get("MONGO_PORT"))
        self.mongo_db_name = os.environ.get("MONGO_DB_NAME")

        # process config
        self.kitchen_simulator_interval = float(os.environ.get("KITCHEN_SIMULATOR_INTERVAL"))
        self.etl_interval = int(os.environ.get("ETL_INTERVAL"))

    def get_postgres_db_uri(self):
        return get_postgres_db_uri(
            self.postgres_user,
            self.postgres_password,
            self.postgres_host,
            self.postgres_db_name,
        )


ENV_CONTEXT_MAP = {"env_config": None}


def get_env_config_instance():

    if not ENV_CONTEXT_MAP["env_config"]:
        ENV_CONTEXT_MAP["env_config"] = EnvConfig()

    return ENV_CONTEXT_MAP["env_config"]

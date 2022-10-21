from injector import Module, provider, singleton

from src.api.controllers.chef_controller import ChefController
from src.core.sqlalchemy_config import get_engine
from sqlalchemy.engine.base import Engine

from src.lib.repositories.impl_v2.chef_repository_impl import ChefRepositoryImpl


class DiProviders(Module):
    @singleton
    @provider
    def get_engine(self) -> Engine:
        return get_engine()

    def configure(self, binder):
        binder.bind(ChefRepositoryImpl, scope=singleton)
        binder.bind(ChefController, scope=singleton)

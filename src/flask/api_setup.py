from injector import Injector

from src.core.di_config import DiProviders
from src.flask.routes.chef import setup_chef_routes


def setup_api(app):
    # ioc instance
    ioc = Injector(DiProviders)

    # blueprints
    chef_blueprint = setup_chef_routes(ioc)

    # register blueprints
    app.register_blueprint(chef_blueprint)

    return app

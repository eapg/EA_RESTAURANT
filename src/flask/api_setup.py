from injector import Injector

from src.core.di_config import DiProviders
from src.flask.routes.chef import setup_chef_routes
from src.flask.routes.ingredient import setup_ingredient_routes
from src.flask.routes.inventory_ingredient import setup_inventory_ingredient_routes
from src.flask.routes.inventory import setup_inventory_routes
from src.flask.routes.order_detail import setup_order_detail_routes


def setup_api(app):
    # ioc instance
    ioc = Injector(DiProviders)

    # blueprints
    chef_blueprint = setup_chef_routes(ioc)
    ingredient_blueprint = setup_ingredient_routes(ioc)
    inventory_ingredient_blueprint = setup_inventory_ingredient_routes(ioc)
    inventory_blueprint = setup_inventory_routes(ioc)
    order_detail_blueprint = setup_order_detail_routes(ioc)

    # register blueprints
    app.register_blueprint(chef_blueprint)
    app.register_blueprint(ingredient_blueprint)
    app.register_blueprint(inventory_ingredient_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(order_detail_blueprint)

    return app

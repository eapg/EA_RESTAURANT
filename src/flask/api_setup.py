from injector import Injector

from src.core.di_config import DiProviders
from src.flask.routes.security_route_middleware import setup_security_route_middleware
from src.flask.routes.chef import setup_chef_routes
from src.flask.routes.ingredient import setup_ingredient_routes
from src.flask.routes.inventory_ingredient import setup_inventory_ingredient_routes
from src.flask.routes.inventory import setup_inventory_routes
from src.flask.routes.order_detail import setup_order_detail_routes
from src.flask.routes.order import setup_order_routes
from src.flask.routes.product_ingredient import setup_product_ingredient_routes
from src.flask.routes.product import setup_product_routes
from src.flask.routes.order_status_history import setup_order_status_history_routes


def setup_api(app):
    # ioc instance
    ioc = Injector(DiProviders)

    # blueprints
    security_route_middleware_blueprint = setup_security_route_middleware(ioc)
    chef_blueprint = setup_chef_routes(ioc)
    ingredient_blueprint = setup_ingredient_routes(ioc)
    inventory_ingredient_blueprint = setup_inventory_ingredient_routes(ioc)
    inventory_blueprint = setup_inventory_routes(ioc)
    order_detail_blueprint = setup_order_detail_routes(ioc)
    order_blueprint = setup_order_routes(ioc)
    product_ingredient_blueprint = setup_product_ingredient_routes(ioc)
    product_blueprint = setup_product_routes(ioc)
    order_status_history_blueprint = setup_order_status_history_routes(ioc)

    # register blueprints
    app.register_blueprint(security_route_middleware_blueprint)
    app.register_blueprint(chef_blueprint)
    app.register_blueprint(ingredient_blueprint)
    app.register_blueprint(inventory_ingredient_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(order_detail_blueprint)
    app.register_blueprint(order_blueprint)
    app.register_blueprint(product_ingredient_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(order_status_history_blueprint)

    return app

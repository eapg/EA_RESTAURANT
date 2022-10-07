# initial data to test the kitchen simulator
from src.constants.audit import InternalUsers, Status
from src.constants.cooking_type import CookingType
from src.constants.order_status import OrderStatus
from src.core import ioc
from src.tests.utils.fixtures.chef_fixture import build_chef
from src.tests.utils.fixtures.ingredient_fixture import build_ingredient
from src.tests.utils.fixtures.inventory_fixture import build_inventory
from src.tests.utils.fixtures.inventory_ingredient_fixture import \
    build_inventory_ingredient
from src.tests.utils.fixtures.order_detail_fixture import build_order_detail
from src.tests.utils.fixtures.order_fixture import build_order
from src.tests.utils.fixtures.product_fixture import build_product
from src.tests.utils.fixtures.product_ingredient_fixture import \
    build_product_ingredient

instance_ioc = ioc.get_ioc_instance()
ingredient_controller = instance_ioc.get_instance("ingredient_controller")
product_ingredient_controller = instance_ioc.get_instance(
    "product_ingredient_controller"
)
inventory_ingredient_controller = instance_ioc.get_instance(
    "inventory_ingredient_controller"
)
inventory_controller = instance_ioc.get_instance("inventory_controller")
product_controller = instance_ioc.get_instance("product_controller")
chef_controller = instance_ioc.get_instance("chef_controller")
order_detail_controller = instance_ioc.get_instance("order_detail_controller")
order_controller = instance_ioc.get_instance("order_controller")
order_status_history_controller = instance_ioc.get_instance(
    "order_status_history_controller"
)
order_manager = instance_ioc.get_instance("order_manager")


def create_inventory():

    inventory = build_inventory()
    inventory_controller.add(inventory)


def create_ingredients():
    ingredient_cheese = build_ingredient(
        name="cheese",
        description="cheddar cheese",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_cheese)
    ingredient_bread = build_ingredient(
        name="bread",
        description="italian bread",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_bread)
    ingredient_tomato = build_ingredient(
        name="tomato",
        description="roma tomato",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_tomato)
    ingredient_meat = build_ingredient(
        name="meat",
        description="hamburger meat",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_meat)
    ingredient_bacon = build_ingredient(
        name="bacon",
        description="bacon",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_bacon)
    ingredient_pizza_bread = build_ingredient(
        name="pizza bread",
        description="pan pizza",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_pizza_bread)
    ingredient_tomato_sauce = build_ingredient(
        name="tomato sauce",
        description="tomato sauce",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_tomato_sauce)
    ingredient_peperoni = build_ingredient(
        name="peperoni",
        description="medium peperoni",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_peperoni)
    linguine_pasta = build_ingredient(
        name="pasta",
        description="pasta type linguine",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(linguine_pasta)
    ingredient_ground_beef = build_ingredient(
        name="ground beef",
        description="ground beef",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_ground_beef)
    ingredient_wheat_tortilla = build_ingredient(
        name="wheat tortilla",
        description="wheat tortilla for tacos",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_wheat_tortilla)
    ingredient_salad = build_ingredient(
        name="salad",
        description="salad",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_salad)
    ingredient_taco_sauce = build_ingredient(
        name="taco sauce",
        description="spicy sauce for tacos",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_taco_sauce)
    ingredient_sausage = build_ingredient(
        name="sausage",
        description="sausage for hot dog",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_sausage)
    ingredient_ketchup = build_ingredient(
        name="ketchup",
        description="ketchup",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_ketchup)
    ingredient_water = build_ingredient(
        name="water",
        description="water",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_water)
    ingredient_orange = build_ingredient(
        name="orange",
        description="orange",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_orange)
    ingredient_sugar = build_ingredient(
        name="sugar",
        description="white sugar",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    ingredient_controller.add(ingredient_sugar)


def create_inventory_ingredients():
    inventory_1 = inventory_controller.get_by_id(1)

    cheese = ingredient_controller.get_by_id(1)
    inventory_ingredient_cheese = build_inventory_ingredient(
        ingredient_id=cheese.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_cheese)

    bread = ingredient_controller.get_by_id(2)
    inventory_ingredient_bread = build_inventory_ingredient(
        ingredient_id=bread.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_bread)

    tomato = ingredient_controller.get_by_id(3)
    inventory_ingredient_tomato = build_inventory_ingredient(
        ingredient_id=tomato.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_tomato)

    meat = ingredient_controller.get_by_id(4)
    inventory_ingredient_meat = build_inventory_ingredient(
        ingredient_id=meat.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_meat)

    bacon = ingredient_controller.get_by_id(5)
    inventory_ingredient_bacon = build_inventory_ingredient(
        ingredient_id=bacon.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_bacon)

    pizza_bread = ingredient_controller.get_by_id(6)
    inventory_ingredient_pizza_bread = build_inventory_ingredient(
        ingredient_id=pizza_bread.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_pizza_bread)

    tomato_sauce = ingredient_controller.get_by_id(7)
    inventory_ingredient_tomato_sauce = build_inventory_ingredient(
        ingredient_id=tomato_sauce.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_tomato_sauce)

    peperoni = ingredient_controller.get_by_id(8)
    inventory_ingredient_peperoni = build_inventory_ingredient(
        ingredient_id=peperoni.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_peperoni)

    pasta = ingredient_controller.get_by_id(9)
    inventory_ingredient_pasta = build_inventory_ingredient(
        ingredient_id=pasta.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_pasta)

    ground_beef = ingredient_controller.get_by_id(10)
    inventory_ingredient_ground_beef = build_inventory_ingredient(
        ingredient_id=ground_beef.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_ground_beef)

    wheat_tortilla = ingredient_controller.get_by_id(11)
    inventory_ingredient_wheat_tortilla = build_inventory_ingredient(
        ingredient_id=wheat_tortilla.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_wheat_tortilla)

    salad = ingredient_controller.get_by_id(12)
    inventory_ingredient_salad = build_inventory_ingredient(
        ingredient_id=salad.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_salad)

    taco_sauce = ingredient_controller.get_by_id(13)
    inventory_ingredient_taco_sauce = build_inventory_ingredient(
        ingredient_id=taco_sauce.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_taco_sauce)

    sausage = ingredient_controller.get_by_id(14)
    inventory_ingredient_sausage = build_inventory_ingredient(
        ingredient_id=sausage.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_sausage)

    ketchup = ingredient_controller.get_by_id(15)
    inventory_ingredient_ketchup = build_inventory_ingredient(
        ingredient_id=ketchup.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_ketchup)

    water = ingredient_controller.get_by_id(16)
    inventory_ingredient_water = build_inventory_ingredient(
        ingredient_id=water.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_water)

    orange = ingredient_controller.get_by_id(17)
    inventory_ingredient_orange = build_inventory_ingredient(
        ingredient_id=orange.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_orange)

    sugar = ingredient_controller.get_by_id(18)
    inventory_ingredient_sugar = build_inventory_ingredient(
        ingredient_id=sugar.id,
        ingredient_quantity=100,
        inventory_id=inventory_1.id,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    inventory_ingredient_controller.add(inventory_ingredient_sugar)


def create_product():
    product_hamburger = build_product(
        name="hamburger",
        description="bacon cheese burger",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_controller.add(product_hamburger)

    product_pizza = build_product(
        name="peperoni pizza",
        description="peperoni and cheese pizza",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_controller.add(product_pizza)

    product_taco = build_product(
        name="taco",
        description="mexican taco",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_controller.add(product_taco)

    product_pasta = build_product(
        name="bolognese pasta",
        description="bolognese pasta",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_controller.add(product_pasta)

    product_hot_dog = build_product(
        name="hot dog",
        description="hot dog",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_controller.add(product_hot_dog)

    product_orange_juice = build_product(
        name="orange juice",
        description="simply orange juice",
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_controller.add(product_orange_juice)


def create_product_ingredients():

    # ingredients
    cheese = ingredient_controller.get_by_id(1)
    bread = ingredient_controller.get_by_id(2)
    tomato = ingredient_controller.get_by_id(3)
    meat = ingredient_controller.get_by_id(4)
    bacon = ingredient_controller.get_by_id(5)
    pizza_bread = ingredient_controller.get_by_id(6)
    tomato_sauce = ingredient_controller.get_by_id(7)
    peperoni = ingredient_controller.get_by_id(8)
    pasta = ingredient_controller.get_by_id(9)
    ground_beef = ingredient_controller.get_by_id(10)
    wheat_tortilla = ingredient_controller.get_by_id(11)
    salad = ingredient_controller.get_by_id(12)
    taco_sauce = ingredient_controller.get_by_id(13)
    sausage = ingredient_controller.get_by_id(14)
    ketchup = ingredient_controller.get_by_id(15)
    water = ingredient_controller.get_by_id(16)
    orange = ingredient_controller.get_by_id(17)
    sugar = ingredient_controller.get_by_id(18)

    # product hamburger
    product_1 = product_controller.get_by_id(1)

    product_ingredient_cheese = build_product_ingredient(
        product_id=product_1.id,
        ingredient_id=cheese.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_cheese)

    product_ingredient_bread = build_product_ingredient(
        product_id=product_1.id,
        ingredient_id=bread.id,
        quantity=2,
        ingredient_type=CookingType.ROASTING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_bread)

    product_ingredient_tomato = build_product_ingredient(
        product_id=product_1.id,
        ingredient_id=tomato.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_tomato)

    product_ingredient_meat = build_product_ingredient(
        product_id=product_1.id,
        ingredient_id=meat.id,
        quantity=1,
        ingredient_type=CookingType.FRYING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_meat)

    product_ingredient_bacon = build_product_ingredient(
        product_id=product_1.id,
        ingredient_id=bacon.id,
        quantity=2,
        ingredient_type=CookingType.FRYING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_bacon)

    # product Pizza
    product_2 = product_controller.get_by_id(2)

    product_ingredient_pizza_bread = build_product_ingredient(
        product_id=product_2.id,
        ingredient_id=pizza_bread.id,
        quantity=1,
        ingredient_type=CookingType.BAKING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_pizza_bread)

    product_ingredient_pizza_cheese = build_product_ingredient(
        product_id=product_2.id,
        ingredient_id=cheese.id,
        quantity=5,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_pizza_cheese)

    product_ingredient_tomato_sauce = build_product_ingredient(
        product_id=product_2.id,
        ingredient_id=tomato_sauce.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_tomato_sauce)

    product_ingredient_peperoni = build_product_ingredient(
        product_id=product_2.id,
        ingredient_id=peperoni.id,
        quantity=15,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_peperoni)

    # product taco
    product_3 = product_controller.get_by_id(3)

    product_ingredient_wheat_tortilla = build_product_ingredient(
        product_id=product_3.id,
        ingredient_id=wheat_tortilla.id,
        quantity=1,
        ingredient_type=CookingType.ROASTING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_wheat_tortilla)

    product_ingredient_taco_ground_beef = build_product_ingredient(
        product_id=product_3.id,
        ingredient_id=ground_beef.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_taco_ground_beef)

    product_ingredient_taco_tomato = build_product_ingredient(
        product_id=product_3.id,
        ingredient_id=tomato.id,
        quantity=3,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_taco_tomato)

    product_ingredient_taco_salad = build_product_ingredient(
        product_id=product_3.id,
        ingredient_id=salad.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_taco_salad)

    product_ingredient_taco_cheese = build_product_ingredient(
        product_id=product_3.id,
        ingredient_id=cheese.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_taco_cheese)

    product_ingredient_taco_sauce = build_product_ingredient(
        product_id=product_3.id,
        ingredient_id=taco_sauce.id,
        quantity=1,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_taco_sauce)

    # product bolognese pasta
    product_4 = product_controller.get_by_id(4)

    product_ingredient_pasta = build_product_ingredient(
        product_id=product_4.id,
        ingredient_id=pasta.id,
        quantity=2,
        ingredient_type=CookingType.BOILING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_pasta)

    product_ingredient_pasta_tomato_sauce = build_product_ingredient(
        product_id=product_4.id,
        ingredient_id=tomato_sauce.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_pasta_tomato_sauce)

    product_ingredient_pasta_tomato = build_product_ingredient(
        product_id=product_4.id,
        ingredient_id=tomato.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_pasta_tomato)

    product_ingredient_pasta_ground_beef = build_product_ingredient(
        product_id=product_4.id,
        ingredient_id=ground_beef.id,
        quantity=4,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_pasta_ground_beef)

    # product hot dog
    product_5 = product_controller.get_by_id(5)

    product_ingredient_hot_dog_bread = build_product_ingredient(
        product_id=product_5.id,
        ingredient_id=bread.id,
        quantity=1,
        ingredient_type=CookingType.ROASTING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_hot_dog_bread)

    product_ingredient_hot_dog_sausage = build_product_ingredient(
        product_id=product_5.id,
        ingredient_id=sausage.id,
        quantity=1,
        ingredient_type=CookingType.BOILING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_hot_dog_sausage)

    product_ingredient_hot_dog_cheese = build_product_ingredient(
        product_id=product_5.id,
        ingredient_id=cheese.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_hot_dog_cheese)

    product_ingredient_hot_dog_ketchup = build_product_ingredient(
        product_id=product_5.id,
        ingredient_id=ketchup.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_hot_dog_ketchup)

    # product orange juice
    product_6 = product_controller.get_by_id(6)

    product_ingredient_orange = build_product_ingredient(
        product_id=product_6.id,
        ingredient_id=orange.id,
        quantity=4,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_orange)

    product_ingredient_water = build_product_ingredient(
        product_id=product_6.id,
        ingredient_id=water.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_water)

    product_ingredient_sugar = build_product_ingredient(
        product_id=product_6.id,
        ingredient_id=sugar.id,
        quantity=2,
        ingredient_type=CookingType.ADDING,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    product_ingredient_controller.add(product_ingredient_sugar)


def create_order():
    # order 1: hamburger(2) + orange juice(2)
    order_1 = build_order(
        status=OrderStatus.NEW_ORDER,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_controller.add(order_1)
    order_manager.add_to_queue(order_1)

    # order 2: pizza(1) + orange juice(4)
    order_2 = build_order(
        status=OrderStatus.NEW_ORDER,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_controller.add(order_2)
    order_manager.add_to_queue(order_2)

    # order 3: tacos(3) + hot dog(1) + orange juice(4)
    order_3 = build_order(
        status=OrderStatus.NEW_ORDER,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_controller.add(order_3)
    order_manager.add_to_queue(order_3)

    # order 4: bolognese pasta(1) + orange juice(1)
    order_4 = build_order(
        status=OrderStatus.NEW_ORDER,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_controller.add(order_4)
    order_manager.add_to_queue(order_4)

    # order 5: orange juice(2)
    order_5 = build_order(
        status=OrderStatus.NEW_ORDER,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_controller.add(order_5)
    order_manager.add_to_queue(order_5)


def create_order_details():

    # products
    hamburger = product_controller.get_by_id(1)
    pizza = product_controller.get_by_id(2)
    taco = product_controller.get_by_id(3)
    bolognese_pasta = product_controller.get_by_id(4)
    hot_dog = product_controller.get_by_id(5)
    orange_juice = product_controller.get_by_id(6)

    # order details for order 1

    order_1 = order_controller.get_by_id(1)
    order_detail_hamburger = build_order_detail(
        order_id=order_1.id,
        product_id=hamburger.id,
        quantity=2,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_hamburger)

    order_detail_orange_juice_1 = build_order_detail(
        order_id=order_1.id,
        product_id=orange_juice.id,
        quantity=2,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_orange_juice_1)

    # order details for order 2

    order_2 = order_controller.get_by_id(2)

    order_detail_pizza = build_order_detail(
        order_id=order_2.id,
        product_id=pizza.id,
        quantity=1,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_pizza)

    order_detail_orange_juice_2 = build_order_detail(
        order_id=order_2.id,
        product_id=orange_juice.id,
        quantity=4,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_orange_juice_2)

    # order details for order 3

    order_3 = order_controller.get_by_id(3)

    order_detail_tacos = build_order_detail(
        order_id=order_3.id,
        product_id=taco.id,
        quantity=3,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_tacos)

    order_detail_hot_dog = build_order_detail(
        order_id=order_3.id,
        product_id=hot_dog.id,
        quantity=1,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_hot_dog)

    order_detail_orange_juice_3 = build_order_detail(
        order_id=order_3.id,
        product_id=orange_juice.id,
        quantity=4,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_orange_juice_3)

    # order details for order 4

    order_4 = order_controller.get_by_id(4)

    order_detail_bolognese_pasta = build_order_detail(
        order_id=order_4.id,
        product_id=bolognese_pasta.id,
        quantity=1,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_bolognese_pasta)

    order_detail_orange_juice_4 = build_order_detail(
        order_id=order_4.id,
        product_id=orange_juice.id,
        quantity=2,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_orange_juice_4)

    # order details for order 5

    order_5 = order_controller.get_by_id(5)

    order_detail_orange_juice_5 = build_order_detail(
        order_id=order_5.id,
        product_id=orange_juice.id,
        quantity=2,
        entity_status=Status.ACTIVE,
        create_by=InternalUsers.SEEDER,
    )
    order_detail_controller.add(order_detail_orange_juice_5)


def create_chefs():
    chef_principal = build_chef(name="Elido p", chef_skills=5)
    chef_intermediate = build_chef(name="Andres p", chef_skills=3)
    chef_basic = build_chef(name="Juan p", chef_skills=1)

    chef_controller.add(chef_principal)
    chef_controller.add(chef_intermediate)
    chef_controller.add(chef_basic)


def run_initial_data():
    create_inventory()
    create_ingredients()
    create_inventory_ingredients()
    create_product()
    create_product_ingredients()
    create_order()
    create_order_details()
    create_chefs()


if __name__ == "__main__":
    run_initial_data()

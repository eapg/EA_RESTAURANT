# EA_RESTAURANT

## Italian Restaurant

### This is a project to develop an Italian Restaurant. Menu, products, chefs, orders and inventories will be included.

### ENTITIES:

* Product Entity - This entity will be used to create products like pizza, hamburgers, pasta and beverages.
* Ingredient Entity - This entity will be used to create ingredients to make the products of the restaurant.
* Inventory Ingredient Entity - This entity will be used to store the Ingredients and its quantity
* Inventory Entity - This entity will store all the items and their quantities
* Order details Entity - This entity will store all the details of the order .
* Order entity - This order will be used to process the client order.
* Chef entity - This entity will be used to create the different chefs who will work in the restaurant.

### Repositories:

* Generic Repository - This repository will be used as an interface to expose generic methods that could be used by the
  developer in order to implement generic operation over a given entity.
* Product Repository - This repository will be used to implement operations to manages products entities.
* Item Repository - This repository will be used to implement operations to manages items entities.
* Inventory Ingredient Repository - This repository will be used to implement operations to manages inventory 
  ingredients entities.
* Inventory Repository - This repository will be used to implement operations to manages inventory entities.
* Order Repository - This repository will be used to implement operations to manages orders entities.
* Order Detail Repository - This repository will be used to implement operations to manages orders detail entities.
* Chef Repository - This repository will be used to implement operations to manages chef entities.

### Controllers:

* The controllers work as interface between users and repositories. they will respond to users events and 
  make requests to repositories.

UML Diagram:

![UML](https://github.com/eapg/EA_RESTAURANT/blob/feature/updating-readme-file/UML_Diagram.png?raw=true)

## Project Setup

Download and install the following tools:

* [Python 3](https://www.python.org/downloads/)
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [PostgreSQL](https://www.postgresql.org/download/)
* [MongoDb](https://www.mongodb.com/try/download/community)
* [MongoDb Compass](https://www.mongodb.com/products/compass)

### Windows users

* Clone git Repository of this project `EA_RESTAURANT`.
* * Open terminal in pycharm.
* Run command `git checkout -b dev` and then `git pull origin dev`
* In Order to create a virtual environment run `python -m venv .venv` 
* In order to activate an environment run the following command: `.venv\Scripts\activate.bat`
* In order to set python Interpreter config the one installed inside .venv in pycharm ide.
* In order to install library dependency run the following command : `pip install -r requirements.txt`
* In order to update library dependency run the following command : `pip freeze > requirements.txt`
* In order to set Environment variables file :
  * - Use `.env.local.example` file to create the different environment files: local, dev, test. 
  * - choose under which environment you are going to work using command: `SET ENV=local` for local, `SET ENV=test` for
      testing.
  * - Run the script that you want to run under chosen environment.

### setup Data base:
* Create `POSTGRESQL` database with the name: `ea_restaurant` following the next steps:
  * Install postgreSQL 
  * Open `pgAdmin`
  * Go to `tools` and open `Querytool` run command `CREATE DATABASE ea_restaurant`

* Run migrations: 

Executing `alembic upgrade head` in a clean database will execute all migrations
in the orders that migrations were created. Like example image.

![img.png](img.png)

To know more about migrations refer to migrations section.

* Create `MONGODB` database with name: `ea_restaurant` and create a collection with name:`order_status_histories`
following next steps:
  * Install MongoDb and MongoDb Compass
  * Open `MongoDb Compass`
  * Go to `Database` and `create new Database` with the name `ea_restaurant` and the collection `order_status_histories`

### Migrations

This project is Using [Alembic](https://alembic.sqlalchemy.org/en/latest/) for migrations. To
install alembic in your project just run `pip install alembic`

Commands to use alembic:

* Initialize: `alembic init alembic`
* Migration Script: `alembic revision -m "migration scrip name"` This script contains some header
  information, identifiers for the current version and import a basic alembic directives, and empty
  `upgrade()` and `downgrade()` functions.
* Upgrade: `alembic upgrade <target-revision>`
* Downgrade: `alembic downgrade <target-revision>`
* Upgrade to head: `alembic upgrade head` This command executes all migrations from the current point to the last.

### Running tests

This project is using [unittest](https://docs.python.org/3/library/unittest.html) for testing: 
* In order to set enviroment to run test:
  * create a test database example: `ea_restaurant_test`
  * set in console test ENV using `set ENV=test`
  * run migrations in test database using `alembic upgrade head`

To run tests just  run `python -m unittest discover --pattern=*_test.py`

This project is using [coverage](https://coverage.readthedocs.io/en/latest/index.html) for coverage. To run test
coverage just run the commands:
* coverage run: `coverage run -m unittest discover --pattern=*test.py`
* coverage report: `coverage report --include='src/tests/*'`
* coverage html report: `coverage html --include='src/tests/*'`

### Linter and Formatter

This project is using:

* [black](https://pypi.org/project/black/)
* [isort](https://pypi.org/project/isort/)
* [pylint](https://pypi.org/project/pylint/)

Commands:

* Format: `black .`
* Sort imports: `isort .`
* Lint file: `pylint [path-to-file.py]`


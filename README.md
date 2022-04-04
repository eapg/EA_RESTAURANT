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
* Item Repository - This repository will be used to implement operations to manages items entities
* Inventory Ingredient Repository - This repository will be used to implement operations to manages inventory 
  ingredients entities.
* Inventory Repository - This repository will be used to implement operations to manages inventory entities.

UML Diagram:

![UML](https://github.com/eapg/EA_RESTAURANT/blob/feature/inventory-repository/UML_Diagram.png?raw=true)

## Project Setup

Download and install the following tools:

* [Python 3](https://www.python.org/downloads/)
* [PyCharm](https://www.jetbrains.com/pycharm/)
* [MiniConda](https://docs.conda.io/en/latest/miniconda.html)

### Windows users

* Open `miniconda3`.
* Go to the project path
* Run `conda create --prefix=.venv python=3.10.0`

### Running tests

This project is using [unittest](https://docs.python.org/3/library/unittest.html) for testing. To run tests just
run `python -m unittest discover --pattern=*_test.py`

### Linter and Formatter

This project is using:

* [black](https://pypi.org/project/black/)
* [isort](https://pypi.org/project/isort/)
* [pylint](https://pypi.org/project/pylint/)

Commands:

* Format: `black .`
* Sort imports: `isort .`
* Lint file: `pylint [path-to-file.py]`

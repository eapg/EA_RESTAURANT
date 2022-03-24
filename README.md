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

* Generic Repository - This repository will be used as an interface to expose generic methods that could be used by
  the developer in order to implement generic operation over a given entity.
* Product Repository - This repository will be used to implement operations to manages products entities.
* Item Repository - This repository will be used to implement operations to manages items entities
* Inventory Item Repository - This repository will be used to implement operations to manages inventory items entities. 

UML Diagram:

![UML](https://github.com/eapg/EA_RESTAURANT/blob/feature/inventory-item-repository/UML_Diagram.png?raw=true)




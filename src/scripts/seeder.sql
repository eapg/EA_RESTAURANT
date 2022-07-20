-- -- PROCEDURE : seeder
DROP PROCEDURE IF EXISTS seeder;

CREATE PROCEDURE seeder()
LANGUAGE 'plpgsql' AS
$$
BEGIN
  -- create users
  CALL insert_user_with_defaults(
         user_name:='SEEDER',
    user_last_name:='SEEDER',
    user_user_name:='SEEDER', 
         user_role:='SEEDER', 
         user_type:='INTERNAL'
  );
        
  CALL insert_user_with_defaults(
         user_name:='KITCHEN_SIMULATOR',
    user_last_name:='KITCHEN_SIMULATOR',
    user_user_name:='KITCHEN_SIMULATOR',
         user_role:='KITCHEN_SIMULATOR',
         user_type:='INTERNAL'
  );
        
  CALL insert_user_with_defaults(
         user_name:='elido',
    user_last_name:='pena',
    user_user_name:='ep_1234',
         user_role:='CHEF',
         user_type:='INTERNAL'
  );
        
  CALL insert_user_with_defaults(
         user_name:='andres', 
    user_last_name:='gonzalez', 
    user_user_name:='ag_1234', 
         user_role:='CHEF', 
         user_type:='INTERNAL'
  );
        
  CALL insert_user_with_defaults(
         user_name:='juan', 
    user_last_name:='perez', 
    user_user_name:='jp_1234', 
         user_role:='CHEF', 
         user_type:='INTERNAL');

  -- creating inventory
  CALL insert_inventory_with_defaults(
        inventory_name :='ea restaurant inventory', 
    inventory_create_by:=1
   );
 
  -- creating ingredients
  CALL insert_ingredient_with_defaults(
           ingredient_name:='cheese',
    ingredient_description:='cheddar cheese',
      ingredient_create_by:=1
  );
  
  CALL insert_ingredient_with_defaults(
           ingredient_name:='bread',
    ingredient_description:='italian bread',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
           ingredient_name:='tomato',
    ingredient_description:='roma tomato',
      ingredient_create_by:=1
  );

  CALL insert_ingredient_with_defaults(
           ingredient_name:='meat',
    ingredient_description:='hamburger meat',
      ingredient_create_by:=1
  );

  CALL insert_ingredient_with_defaults(
           ingredient_name:='bacon',
    ingredient_description:='bacon',
      ingredient_create_by:=1
  );
  
  CALL insert_ingredient_with_defaults(
           ingredient_name:='pizza bread',
    ingredient_description:='pan pizza',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
           ingredient_name:='tomato sauce',
    ingredient_description:='tomato sauce',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
           ingredient_name:='peperoni',
    ingredient_description:='medium peperoni',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
           ingredient_name:='pasta',
    ingredient_description:='pasta type linguine',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
           ingredient_name:='ground beef',
    ingredient_description:='ground beef',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
           ingredient_name:='wheat tortilla',
    ingredient_description:='wheat tortilla for tacos',
      ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
    ingredient_name:='salad',
    ingredient_description:='salad',
    ingredient_create_by:=1
  );
  
  CALL insert_ingredient_with_defaults(
    ingredient_name:='taco sauce',
    ingredient_description:='spicy sauce for tacos',
    ingredient_create_by:=1
  );
  
  CALL insert_ingredient_with_defaults(
    ingredient_name:='sausage',
    ingredient_description:='sausage for hot dog',
    ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
    ingredient_name:='ketchup',
    ingredient_description:='ketchup',
    ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
    ingredient_name:='water',
    ingredient_description:='water',
    ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
    ingredient_name:='orange',
    ingredient_description:='orange',
    ingredient_create_by:=1
  );
 
  CALL insert_ingredient_with_defaults(
    ingredient_name:='sugar',
    ingredient_description:='white sugar',
    ingredient_create_by:=1
  );
 

  -- creating inventory ingredients
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=1,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  ); 
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=2,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=3,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=4,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=5,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=6,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=7,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=8,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=9,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=10,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=11,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=12,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=13,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=14,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=15,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=16,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=17,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  CALL insert_inventory_ingredient_with_defaults(
    inventory_ingredient_ingredient_id:=18,
     inventory_ingredient_inventory_id:=1, 
         inventory_ingredient_quantity:=100,
        inventory_ingredient_create_by:=1
  );
 
  -- creating products
  CALL insert_product_with_defaults(
           product_name:='hamburger', 
    product_description:='bacon cheese burger', 
      product_create_by:=1
  ); 
 
  CALL insert_product_with_defaults(
           product_name:='peperoni pizza', 
    product_description:='peperoni and cheese pizza', 
      product_create_by:=1
  );
 
  CALL insert_product_with_defaults(
           product_name:='taco', 
    product_description:='mexican taco', 
      product_create_by:=1
  );
 
  CALL insert_product_with_defaults(
           product_name:='bolognese pasta', 
    product_description:='bolognese pasta', 
      product_create_by:=1
  );
 
  CALL insert_product_with_defaults(
           product_name:='hot dog', 
    product_description:='hot dog', 
      product_create_by:=1
  );
 
  CALL insert_product_with_defaults(
           product_name:='orange juice', 
    product_description:='simply orange juice', 
      product_create_by:=1
  );
 
  -- creating product ingredients
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=1,
    product_ingredient_ingredient_id:=1,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=1,
    product_ingredient_ingredient_id:=2,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ROASTING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=1,
    product_ingredient_ingredient_id:=3,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=1,
    product_ingredient_ingredient_id:=4,
         product_ingredient_quantity:=1,
     product_ingredient_cooking_type:='FRYING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=1,
    product_ingredient_ingredient_id:=5,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='FRYING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=2,
    product_ingredient_ingredient_id:=6,
         product_ingredient_quantity:=1,
     product_ingredient_cooking_type:='BAKING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=2,
    product_ingredient_ingredient_id:=1,
         product_ingredient_quantity:=5,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=2,
    product_ingredient_ingredient_id:=7,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=2,
    product_ingredient_ingredient_id:=8,
         product_ingredient_quantity:=15,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=3,
    product_ingredient_ingredient_id:=11,
         product_ingredient_quantity:=1,
     product_ingredient_cooking_type:='ROASTING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=3,
    product_ingredient_ingredient_id:=10,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=3,
    product_ingredient_ingredient_id:=3,
         product_ingredient_quantity:=3,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=3,
    product_ingredient_ingredient_id:=12,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=3,
    product_ingredient_ingredient_id:=1,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=3,
    product_ingredient_ingredient_id:=13,
         product_ingredient_quantity:=1,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=4,
    product_ingredient_ingredient_id:=9,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='BOILING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=4,
    product_ingredient_ingredient_id:=7,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=4,
    product_ingredient_ingredient_id:=3,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=4,
    product_ingredient_ingredient_id:=10,
         product_ingredient_quantity:=4,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=5,
    product_ingredient_ingredient_id:=2,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ROASTING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=5,
    product_ingredient_ingredient_id:=14,
         product_ingredient_quantity:=1,
     product_ingredient_cooking_type:='BOILING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=5,
    product_ingredient_ingredient_id:=1,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=5,
    product_ingredient_ingredient_id:=15,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=6,
    product_ingredient_ingredient_id:=17,
         product_ingredient_quantity:=4,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=6,
    product_ingredient_ingredient_id:=16,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  CALL insert_product_ingredient_with_defaults(
       product_ingredient_product_id:=6,
    product_ingredient_ingredient_id:=18,
         product_ingredient_quantity:=2,
     product_ingredient_cooking_type:='ADDING',
        product_ingredient_create_by:=1
  );
  
  -- creating orders
  CALL insert_order_with_defaults(
       order_status:='NEW_ORDER',
    order_create_by:=1
  ); 
 
  CALL insert_order_with_defaults(
       order_status:='NEW_ORDER',
    order_create_by:=1
  ); 
 
  CALL insert_order_with_defaults(
       order_status:='NEW_ORDER',
    order_create_by:=1
  ); 
 
  CALL insert_order_with_defaults(
       order_status:='NEW_ORDER',
    order_create_by:=1
  ); 
 
  CALL insert_order_with_defaults(
       order_status:='NEW_ORDER',
    order_create_by:=1
  );
 
  -- creating order details
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=1,
    order_detail_product_id:=1,
      order_detail_quantity:=2,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=1,
    order_detail_product_id:=6,
      order_detail_quantity:=2,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=2,
    order_detail_product_id:=2,
      order_detail_quantity:=1,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=2,
    order_detail_product_id:=6,
      order_detail_quantity:=4,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=3,
    order_detail_product_id:=3,
      order_detail_quantity:=3,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=3,
    order_detail_product_id:=5,
      order_detail_quantity:=1,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=3,
    order_detail_product_id:=6,
      order_detail_quantity:=1,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=4,
    order_detail_product_id:=4,
      order_detail_quantity:=1,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=4,
    order_detail_product_id:=6,
      order_detail_quantity:=2,
     order_detail_create_by:=1
  );
 
  CALL insert_order_detail_with_defaults(
      order_detail_order_id:=5,
    order_detail_product_id:=6,
      order_detail_quantity:=2,
     order_detail_create_by:=1
  );
 
  -- creating chefs
  CALL insert_chef_with_defaults(
    chef_user_id:=3, 
      chef_skill:=1,chef_create_by:=1
  ); 
 
  CALL insert_chef_with_defaults(
    chef_user_id:=4, 
      chef_skill:=1,chef_create_by:=1
  );
 
  CALL insert_chef_with_defaults(
    chef_user_id:=5, 
      chef_skill:=1,chef_create_by:=1
  );

END;
$$;



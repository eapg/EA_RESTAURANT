-- DATABASE : ea_restaurant
DROP DATABASE IF EXISTS ea_restaurant;

CREATE DATABASE ea_restaurant;

-- Enum : status
DROP TYPE IF EXISTS status_enum CASCADE;

CREATE TYPE status_enum AS ENUM ('ACTIVE', 'DELETE');

-- Table : products
DROP TABLE IF EXISTS products;

CREATE TABLE products(
             id BIGSERIAL NOT NULL ,
           name VARCHAR(50) NOT NULL,
    description VARCHAR(100) DEFAULT '',
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Enum : user_type_enum
DROP TYPE IF EXISTS user_type_enum CASCADE;

CREATE TYPE user_type_enum AS ENUM ('INTERNAL','EXTERNAL');

-- Enum : user_role_enum
DROP TYPE IF EXISTS user_role_enum

CREATE TYPE user_role_enum AS ENUM ('CHEF', 'CLIENT', 'CASHIER', 'SEEDER', 'KITCHEN_SIMULATOR')

-- Table : users
DROP TABLE IF EXISTS users;

CREATE TABLE users(
             id BIGSERIAL NOT NULL,
           name VARCHAR(50) NOT NULL,
      last_name VARCHAR(50) NOT NULL,
       user_name VARCHAR(50) NOT NULL,
       password VARCHAR(500) NOT NULL,
           role user_role_enum NOT NULL,
           type user_type_enum NOT NULL,
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
 );

-- Enum : cooking_type_enum
DROP TYPE IF EXISTS cooking_type_enum CASCADE;

CREATE TYPE cooking_type_enum AS ENUM ('ADDING', 'ROASTING', 'BOILING', 'BAKING', 'FRYING', 'HEADING', 'PREPARING_DRINK');

-- Table : product_ingredients
DROP TABLE IF EXISTS product_ingredients;

CREATE TABLE product_ingredients(
             id BIGSERIAL NOT NULL,
     product_id BIGINT NOT NULL,
  ingredient_id BIGINT NOT NULL,
       quantity INTEGER NOT NULL,
   cooking_type cooking_type_enum NOT NULL,
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Table : ingredients
DROP TABLE IF EXISTS ingredients;

CREATE TABLE ingredients(
             id BIGSERIAL NOT NULL,
           name VARCHAR(50) NOT NULL,
    description VARCHAR(100) DEFAULT '',
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Table : inventory_ingredients
DROP TABLE IF EXISTS inventory_ingredients;

CREATE TABLE inventory_ingredients(
             id BIGSERIAL NOT NULL,
  ingredient_id BIGINT NOT NULL,
   inventory_id BIGINT NOT NULL,
       quantity INTEGER NOT NULL,
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Table : inventories
DROP TABLE IF EXISTS inventories;


CREATE TABLE inventories(
             id BIGSERIAL NOT NULL,
           name VARCHAR(50) NOT NULL,
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Enum : order_status_enum
DROP TYPE IF EXISTS order_status_enum CASCADE;

CREATE TYPE order_status_enum AS ENUM ('NEW_ORDER', 'IN_PROCESS', 'COMPLETED', 'CANCELLED');

-- Table : Orders 
DROP TABLE IF EXISTS orders;

CREATE TABLE orders(
                id BIGSERIAL NOT NULL,
            status order_status_enum NOT NULL,
  assigned_chef_id BIGINT NOT NULL,
     entity_status status_enum NOT NULL,
         create_by BIGINT NOT NULL,
       create_date TIMESTAMP WITHOUT TIME ZONE,
         update_by BIGINT NOT NULL,
       update_date TIMESTAMP WITHOUT TIME ZONE,
           PRIMARY KEY (id)
);

-- Table : order_details
DROP TABLE IF EXISTS order_details;

CREATE TABLE order_details(
             id BIGSERIAL NOT NULL,
       order_id BIGINT NOT NULL,
     product_id BIGINT NOT NULL,
       quantity INTEGER NOT NULL,
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Table : order_status_histories 
DROP TABLE IF EXISTS order_status_histories;

CREATE TABLE order_status_histories(
             id BIGSERIAL NOT NULL,
       order_id BIGINT NOT NULL,
      from_time TIMESTAMP WITHOUT TIME ZONE,
        to_time TIMESTAMP WITHOUT TIME ZONE,
    from_status order_status_enum,
      to_status order_status_enum,
  entity_status status_enum NOT NULL,
      create_by BIGINT NOT NULL,
    create_date TIMESTAMP WITHOUT TIME ZONE,
      update_by BIGINT NOT NULL,
    update_date TIMESTAMP WITHOUT TIME ZONE,
        PRIMARY KEY (id)
);

-- Table : chefs 
DROP TABLE IF EXISTS chefs;

CREATE TABLE chefs(
              id BIGSERIAL NOT NULL,
         user_id BIGINT NOT NULL,
           skill INTEGER NOT NULL,
   entity_status status_enum NOT NULL,
       create_by BIGINT NOT NULL,
     create_date TIMESTAMP WITHOUT TIME ZONE,
       update_by BIGINT NOT NULL,
     update_date TIMESTAMP WITHOUT TIME ZONE,
         PRIMARY KEY (id)
);

-- constraints for table relations

-- constraints for products table
ALTER TABLE products 
  ADD CONSTRAINT fk_product_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE products 
  ADD CONSTRAINT fk_product_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);

-- constraints for product_ingredients table     
ALTER TABLE product_ingredients 
  ADD CONSTRAINT fk_product_ingredient_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE product_ingredients 
  ADD CONSTRAINT fk_product_ingredient_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);
     
ALTER TABLE product_ingredients 
  ADD CONSTRAINT fk_product_ingredient_ingredient FOREIGN KEY (ingredient_id) 
      REFERENCES ingredients (id);

ALTER TABLE product_ingredients
  ADD CONSTRAINT fk_product_ingredient_product FOREIGN KEY (product_id)    
      REFERENCES products (id);

-- constraints for ingredients table     
ALTER TABLE ingredients 
  ADD CONSTRAINT fk_ingredient_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE ingredients 
  ADD CONSTRAINT fk_ingredient_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);

-- constraints for inventory_ingredients table     
ALTER TABLE inventory_ingredients 
  ADD CONSTRAINT fk_inventory_ingredient_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE inventory_ingredients 
  ADD CONSTRAINT fk_inventory_ingredient_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);
     
ALTER TABLE inventory_ingredients
  ADD CONSTRAINT fk_inventory_ingredient_ingredient FOREIGN KEY (ingredient_id)
      REFERENCES ingredients (id);

ALTER TABLE inventory_ingredients     
  ADD CONSTRAINT fk_inventory_ingredient_inventory FOREIGN KEY (inventory_id)
      REFERENCES inventories (id);

-- constraints for inventories table      
ALTER TABLE inventories 
  ADD CONSTRAINT fk_inventory_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE inventories 
  ADD CONSTRAINT fk_inventory_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);

-- constraints for orders table      
ALTER TABLE orders 
  ADD CONSTRAINT fk_order_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE orders 
  ADD CONSTRAINT fk_order_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);

ALTER TABLE orders 
  ADD CONSTRAINT fk_order_chef FOREIGN KEY (assigned_chef_id)
      REFERENCES chefs (id);

-- constraints for order_details table     
ALTER TABLE order_details 
  ADD CONSTRAINT fk_order_detail_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE order_details 
  ADD CONSTRAINT fk_order_detail_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);
  
ALTER TABLE order_details
  ADD CONSTRAINT fk_order_detail_order FOREIGN KEY (order_id)
      REFERENCES orders (id);
     
ALTER TABLE order_details     
  ADD CONSTRAINT fk_order_detail_product FOREIGN KEY (product_id)
      REFERENCES products (id);

-- constraints for order_status_histories table      
ALTER TABLE order_status_histories 
  ADD CONSTRAINT fk_order_status_history_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE order_status_histories 
  ADD CONSTRAINT fk_order_status_history_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);

ALTER TABLE order_status_histories
  ADD CONSTRAINT fk_order_status_history_order FOREIGN KEY (order_id)
      REFERENCES orders (id);

-- constraints for chefs table      
ALTER TABLE chefs 
  ADD CONSTRAINT fk_chef_user_create FOREIGN KEY (create_by)
      REFERENCES users(id);
     
ALTER TABLE chefs 
  ADD CONSTRAINT fk_chef_user_update FOREIGN KEY (update_by)
      REFERENCES users(id);
     
ALTER TABLE chefs
  ADD CONSTRAINT fk_chef_user FOREIGN KEY (user_id)
      REFERENCES users (id);




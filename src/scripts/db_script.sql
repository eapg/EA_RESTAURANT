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
           name VARCHAR(20) NOT NULL,
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

-- Table : users
DROP TABLE IF EXISTS users;

CREATE TABLE users(
             id BIGSERIAL NOT NULL,
           name VARCHAR(50) NOT NULL,
      last_name VARCHAR(50) NOT NULL,
       username VARCHAR(50) NOT NULL,
       password VARCHAR(500) NOT NULL,
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
DROP TABLE IF EXISTS product_ingredients

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
DROP TABLE IF EXISTS ingredients

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
DROP TABLE IF EXISTS inventory_ingredient;

CREATE TABLE inventory_ingredient(
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
DROP TABLE IF EXISTS orders:

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


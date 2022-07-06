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
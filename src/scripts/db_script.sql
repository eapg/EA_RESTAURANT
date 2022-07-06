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

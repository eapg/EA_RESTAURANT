-- FUNCTION : product_fixture
DROP PROCEDURE IF EXISTS insert_product_with_defaults;

CREATE PROCEDURE insert_product_with_defaults(
           product_name VARCHAR(50) DEFAULT 'test_product',
    product_description VARCHAR(100) DEFAULT 'test_description',
  product_entity_status status_enum DEFAULT 'ACTIVE',
      product_create_by BIGINT DEFAULT 1,
    product_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      product_update_by BIGINT DEFAULT 1,
    product_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO products
              (
                name,
                description,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                product_name,
                product_description,
                product_entity_status,
                product_create_by,
                product_create_date,
                product_update_by,
                product_update_date
              );
END;
$$;


-- PROCEDURE : user_fixture
DROP PROCEDURE IF EXISTS insert_user_with_defaults;

CREATE PROCEDURE insert_user_with_defaults(
           user_name VARCHAR(50) DEFAULT 'elido',
      user_last_name VARCHAR(50) DEFAULT 'pena'
      user_user_name VARCHAR(50) DEFAULT 'test_user',
       user_password VARCHAR(500) DEFAULT '1234',
           user_type user_type_enum DEFAULT 'INTERNAL',
  user_entity_status status_enum DEFAULT 'ACTIVE',
      user_create_by BIGINT DEFAULT 1,
    user_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      user_update_by BIGINT DEFAULT 1,
    user_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO products
              (
                name,
                last_name,
                user_name,
                password,
                type,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                user_name,
                user_last_name,
                user_user_name,
                user_password,
                user_type,
                user_entity_status,
                user_create_by,
                user_create_date,
                user_update_by,
                user_update_date
              );
END;
$$;

-- PROCEDURE : product_ingredient_fixture
DROP PROCEDURE IF EXISTS insert_product_ingredient_with_defaults;

CREATE PROCEDURE insert_product_ingredient_with_defaults(
     product_ingredient_product_id BIGINT DEFAULT 1,
  product_ingredient_ingredient_id BIGINT DEFAULT 1,
       product_ingredient_quantity INTEGER DEFAULT 1,
   product_ingredient_cooking_type cooking_type_enum DEFAULT 'ADDING',
  product_ingredient_entity_status status_enum DEFAULT 'ACTIVE',
      product_ingredient_create_by BIGINT DEFAULT 1,
    product_ingredient_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      product_ingredient_update_by BIGINT DEFAULT 1,
    product_ingredient_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO products
              (
                product_id,
                ingredient_id,
                quantity,
                cooking_type,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                product_ingredient_product_id,
                product_ingredient_ingredient_id,
                product_ingredient_quantity,
                product_ingredient_cooking_type,
                product_ingredient_entity_status,
                product_ingredient_create_by,
                product_ingredient_create_date,
                product_ingredient_update_by,
                product_ingredient_update_date
              );
END;
$$;

-- PROCEDURE : ingredient_fixture
DROP PROCEDURE IF EXISTS insert_ingredient_with_defaults;

CREATE PROCEDURE insert_ingredient_with_defaults(
           ingredient_name VARCHAR(50) DEFAULT 'test_ingredient',
    ingredient_description VARCHAR(100) DEFAULT 'test_description',
  ingredient_entity_status status_enum DEFAULT 'ACTIVE',
      ingredient_create_by BIGINT DEFAULT 1,
    ingredient_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      ingredient_update_by BIGINT DEFAULT 1,
    ingredient_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO products
              (
                name,
                description,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                ingredient_name,
                ingredient_description,
                ingredient_entity_status,
                ingredient_create_by,
                ingredient_create_date,
                ingredient_update_by,
                ingredient_update_date
              );
END;
$$;

-- PROCEDURE : inventory_ingredient_fixture
DROP PROCEDURE IF EXISTS insert_inventory_ingredient_with_defaults;

CREATE PROCEDURE insert_inventory_ingredient_with_defaults(
  inventory_ingredient_ingredient_id BIGINT DEFAULT 1,
   inventory_ingredient_inventory_id BIGINT DEFAULT 1,
       inventory_ingredient_quantity INTEGER DEFAULT 1,
            ingredient_entity_status status_enum DEFAULT 'ACTIVE',
                ingredient_create_by BIGINT DEFAULT 1,
              ingredient_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                ingredient_update_by BIGINT DEFAULT 1,
              ingredient_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO inventory_ingredients
              (
                ingredient_id,
                inventory_id,
                quantity,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                inventory_ingredient_ingredient_id,
                inventory_ingredient_inventory_id,
                inventory_ingredient_quantity,
                inventory_ingredient_entity_status,
                inventory_ingredient_create_by,
                inventory_ingredient_create_date,
                inventory_ingredient_update_by,
                inventory_ingredient_update_date
              );
END;
$$;

-- PROCEDURE : inventory_fixture
DROP PROCEDURE IF EXISTS insert_inventory_with_defaults;

CREATE PROCEDURE insert_inventory_with_defaults(
           inventory_name VARCHAR(50) DEFAULT 'test_inventory',
  inventory_entity_status status_enum DEFAULT 'ACTIVE',
      inventory_create_by BIGINT DEFAULT 1,
    inventory_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      inventory_update_by BIGINT DEFAULT 1,
    inventory_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO inventories
              (
                name,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                inventory_name,
                inventory_entity_status,
                inventory_create_by,
                inventory_create_date,
                inventory_update_by,
                inventory_update_date
              );
END;
$$;

-- PROCEDURE : order_fixture
DROP PROCEDURE IF EXISTS insert_order_with_defaults;

CREATE PROCEDURE insert_order_with_defaults(
            order_status order_status_enum defaul 'NEW_ORDER',
  order_assigned_chef_id BIGINT DEFAULT 1,
     order_entity_status status_enum DEFAULT 'ACTIVE',
         order_create_by BIGINT DEFAULT 1,
       order_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         order_update_by BIGINT DEFAULT 1,
       order_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO orders
              (
                status,
                assigned_chef_id,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                order_status,
                order_assigned_chef_id,
                order_entity_status,
                order_create_by,
                order_create_date,
                order_update_by,
                order_update_date
              );
END;
$$;

-- PROCEDURE : order_detail_fixture
DROP PROCEDURE IF EXISTS insert_order_detail_with_defaults;

CREATE PROCEDURE insert_order_detail_with_defaults(
       order_detail_order_id BIGINT DEFAULT 1,
     order_detail_product_id BIGINT DEFAULT 1,
       order_detail_quantity INTEGER DEFAULT 1,
  order_detail_entity_status status_enum DEFAULT 'ACTIVE',
      order_detail_create_by BIGINT DEFAULT 1,
    order_detail_create_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      order_detail_update_by BIGINT DEFAULT 1,
    order_detail_update_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO order_details
              (
                order_id,
                product_id,
                quantity,
                entity_status,
                create_by,
                create_date,
                update_by,
                update_date
              )
       VALUES (
                order_detail_order_id,
                order_detail_product_id,
                order_detail_quantity,
                order_detail_entity_status,
                order_detail_create_by,
                order_detail_create_date,
                order_detail_update_by,
                order_detail_update_date
              );
END;
$$;

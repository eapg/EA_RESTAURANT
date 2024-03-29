
DROP PROCEDURE IF EXISTS insert_product_with_defaults;

CREATE PROCEDURE insert_product_with_defaults(
           product_name VARCHAR(50) DEFAULT 'test_product',
    product_description VARCHAR(100) DEFAULT 'test_description',
  product_entity_status status_enum DEFAULT 'ACTIVE',
      product_created_by BIGINT DEFAULT 1,
    product_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      product_updated_by BIGINT DEFAULT 1,
    product_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO products
              (
                name,
                description,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                product_name,
                product_description,
                product_entity_status,
                product_created_by,
                product_created_date,
                product_updated_by,
                product_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_user_with_default;

CREATE PROCEDURE insert_user_with_defaults(
           user_name VARCHAR(50) DEFAULT 'elido',
      user_last_name VARCHAR(50) DEFAULT 'pena',
      user_user_name VARCHAR(50) DEFAULT 'test_user',
       user_password VARCHAR(500) DEFAULT '1234',
           user_role user_role_enum DEFAULT 'SEEDER',
           user_type user_type_enum DEFAULT 'INTERNAL',
  user_entity_status status_enum DEFAULT 'ACTIVE',
      user_created_by BIGINT DEFAULT 1,
    user_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      user_updated_by BIGINT DEFAULT 1,
    user_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO users
              (
                name,
                last_name,
                user_name,
                password,
                role,
                type,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                user_name,
                user_last_name,
                user_user_name,
                user_password,
                user_role,
                user_type,
                user_entity_status,
                user_created_by,
                user_created_date,
                user_updated_by,
                user_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_product_ingredient_with_defaults;

CREATE PROCEDURE insert_product_ingredient_with_defaults(
     product_ingredient_product_id BIGINT DEFAULT 1,
  product_ingredient_ingredient_id BIGINT DEFAULT 1,
       product_ingredient_quantity INTEGER DEFAULT 1,
   product_ingredient_cooking_type cooking_type_enum DEFAULT 'ADDING',
  product_ingredient_entity_status status_enum DEFAULT 'ACTIVE',
      product_ingredient_created_by BIGINT DEFAULT 1,
    product_ingredient_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      product_ingredient_updated_by BIGINT DEFAULT 1,
    product_ingredient_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO product_ingredients
              (
                product_id,
                ingredient_id,
                quantity,
                cooking_type,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                product_ingredient_product_id,
                product_ingredient_ingredient_id,
                product_ingredient_quantity,
                product_ingredient_cooking_type,
                product_ingredient_entity_status,
                product_ingredient_created_by,
                product_ingredient_created_date,
                product_ingredient_updated_by,
                product_ingredient_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_ingredient_with_defaults;

CREATE PROCEDURE insert_ingredient_with_defaults(
           ingredient_name VARCHAR(50) DEFAULT 'test_ingredient',
    ingredient_description VARCHAR(100) DEFAULT 'test_description',
  ingredient_entity_status status_enum DEFAULT 'ACTIVE',
      ingredient_created_by BIGINT DEFAULT 1,
    ingredient_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      ingredient_updated_by BIGINT DEFAULT 1,
    ingredient_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO ingredients 
              (
                name,
                description,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                ingredient_name,
                ingredient_description,
                ingredient_entity_status,
                ingredient_created_by,
                ingredient_created_date,
                ingredient_updated_by,
                ingredient_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_inventory_ingredient_with_defaults;

CREATE PROCEDURE insert_inventory_ingredient_with_defaults(
  inventory_ingredient_ingredient_id BIGINT DEFAULT 1,
   inventory_ingredient_inventory_id BIGINT DEFAULT 1,
       inventory_ingredient_quantity INTEGER DEFAULT 1,
  inventory_ingredient_entity_status status_enum DEFAULT 'ACTIVE',
      inventory_ingredient_created_by BIGINT DEFAULT 1,
    inventory_ingredient_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      inventory_ingredient_updated_by BIGINT DEFAULT 1,
    inventory_ingredient_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                inventory_ingredient_ingredient_id,
                inventory_ingredient_inventory_id,
                inventory_ingredient_quantity,
                inventory_ingredient_entity_status,
                inventory_ingredient_created_by,
                inventory_ingredient_created_date,
                inventory_ingredient_updated_by,
                inventory_ingredient_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_inventory_with_defaults;

CREATE PROCEDURE insert_inventory_with_defaults(
           inventory_name VARCHAR(50) DEFAULT 'test_inventory',
  inventory_entity_status status_enum DEFAULT 'ACTIVE',
      inventory_created_by BIGINT DEFAULT 1,
    inventory_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      inventory_updated_by BIGINT DEFAULT 1,
    inventory_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO inventories
              (
                name,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                inventory_name,
                inventory_entity_status,
                inventory_created_by,
                inventory_created_date,
                inventory_updated_by,
                inventory_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_order_with_defaults;

CREATE PROCEDURE insert_order_with_defaults(
            order_status order_status_enum DEFAULT 'NEW_ORDER',
  order_assigned_chef_id BIGINT DEFAULT 1,
     order_entity_status status_enum DEFAULT 'ACTIVE',
         order_created_by BIGINT DEFAULT 1,
       order_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
         order_updated_by BIGINT DEFAULT 1,
       order_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO orders
              (
                status,
                assigned_chef_id,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                order_status,
                order_assigned_chef_id,
                order_entity_status,
                order_created_by,
                order_created_date,
                order_updated_by,
                order_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_order_detail_with_defaults;

CREATE PROCEDURE insert_order_detail_with_defaults(
       order_detail_order_id BIGINT DEFAULT 1,
     order_detail_product_id BIGINT DEFAULT 1,
       order_detail_quantity INTEGER DEFAULT 1,
  order_detail_entity_status status_enum DEFAULT 'ACTIVE',
      order_detail_created_by BIGINT DEFAULT 1,
    order_detail_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      order_detail_updated_by BIGINT DEFAULT 1,
    order_detail_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                order_detail_order_id,
                order_detail_product_id,
                order_detail_quantity,
                order_detail_entity_status,
                order_detail_created_by,
                order_detail_created_date,
                order_detail_updated_by,
                order_detail_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_order_status_history_with_defaults;

CREATE PROCEDURE insert_order_status_history_with_defaults(
       order_status_history_order_id BIGINT DEFAULT 1,
      order_status_history_from_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        order_status_history_to_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    order_status_history_from_status order_status_enum DEFAULT 'NEW_ORDER',
      order_status_history_to_status order_status_enum DEFAULT 'IN_PROCESS',
  order_status_history_entity_status status_enum DEFAULT 'ACTIVE',
      order_status_history_created_by BIGINT DEFAULT 1,
    order_status_history_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      order_status_history_updated_by BIGINT DEFAULT 1,
    order_status_history_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO order_status_histories
              (
                order_id,
                from_time,
                to_time,
                from_status,
                to_status,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                order_status_history_order_id,
                order_status_history_from_time,
                order_status_history_to_time,
                order_status_history_from_status,
                order_status_history_to_status,
                order_status_history_entity_status,
                order_status_history_created_by,
                order_status_history_created_date,
                order_status_history_updated_by,
                order_status_history_updated_date
              );
END;
$$;


DROP PROCEDURE IF EXISTS insert_chef_with_defaults;

CREATE PROCEDURE insert_chef_with_defaults(
        chef_user_id BIGINT DEFAULT 3,
          chef_skill INTEGER DEFAULT 1,
  chef_entity_status status_enum DEFAULT 'ACTIVE',
      chef_created_by BIGINT DEFAULT 1,
    chef_created_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
      chef_updated_by BIGINT DEFAULT 1,
    chef_updated_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
)
LANGUAGE 'plpgsql' AS
$$
BEGIN
  INSERT INTO chefs
              (
                user_id,
                skill,
                entity_status,
                created_by,
                created_date,
                updated_by,
                updated_date
              )
       VALUES (
                chef_user_id,
                chef_skill,
                chef_entity_status,
                chef_created_by,
                chef_created_date,
                chef_updated_by,
                chef_updated_date
              );
END;
$$;

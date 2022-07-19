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




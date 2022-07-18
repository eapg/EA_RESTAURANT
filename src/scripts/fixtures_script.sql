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

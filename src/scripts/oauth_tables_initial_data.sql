INSERT INTO app_clients(
  client_name,
  client_id,
  client_secret,
  access_token_expiration_time,
  refresh_token_expiration_time,
  entity_status,
  created_by,
  created_date,
  updated_by,
  updated_date
  )
  VALUES(
    'postman',
    'postman001',
    '$2a$12$rb1quyHV8c.R4iEE5PlRme/lFZrn3uO2ri1stG7EM1EPa8ZRk2ptC',
    300,
    900,
    'ACTIVE',
    1,
    CURRENT_TIMESTAMP,
    1,
    CURRENT_TIMESTAMP
 );

INSERT INTO app_clients_scopes(
  app_client_id,
  scope,
  entity_status,
  created_by,
  created_date,
  updated_by,
  updated_date
)
VALUES(
  1,
  'READ/WRITE',
  'ACTIVE',
  1,
  CURRENT_TIMESTAMP,
  1,
  CURRENT_TIMESTAMP 
);

INSERT INTO app_client_users(
  app_client_id,
  user_name,
  entity_status,
  created_by,
  created_date,
  updated_by,
  updated_date
)

VALUES(
  1,
  'ep_1234',
  'ACTIVE',
  1,
  CURRENT_TIMESTAMP,
  1,
  CURRENT_TIMESTAMP 
  );
 

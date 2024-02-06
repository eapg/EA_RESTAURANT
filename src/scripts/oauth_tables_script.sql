
DROP TABLE IF EXISTS app_clients CASCADE;

CREATE TABLE app_clients(
             id BIGSERIAL NOT NULL,
             client_name VARCHAR(50) NOT NULL,
             client_id TEXT  NOT NULL,
             client_secret TEXT NOT NULL,
             access_token_expiration_time INT NOT NULL,
             refresh_token_expiration_time INT NOT NULL,
             entity_status status_enum NOT NULL,
             created_by BIGINT NOT NULL,
             created_date TIMESTAMP WITHOUT TIME ZONE,
             updated_by BIGINT NOT NULL,
             updated_date TIMESTAMP WITHOUT TIME ZONE,
             PRIMARY KEY (id)
);

DROP TYPE IF EXISTS scope_enum CASCADE;

CREATE TYPE scope_enum AS ENUM ('READ','WRITE', 'READ/WRITE');

DROP TABLE IF EXISTS app_clients_scopes CASCADE;

CREATE TABLE app_clients_scopes(
             id BIGSERIAL NOT NULL,
             app_client_id BIGINT NOT NULL,
             scope scope_enum NOT NULL,
             entity_status status_enum NOT NULL,
             created_by BIGINT NOT NULL,
             created_date TIMESTAMP WITHOUT TIME ZONE,
             updated_by BIGINT NOT NULL,
             updated_date TIMESTAMP WITHOUT TIME ZONE,
             PRIMARY KEY (id)
);


DROP TABLE IF EXISTS client_users CASCADE;

CREATE TABLE app_client_users(
             id BIGSERIAL NOT NULL,
             app_client_id BIGINT NOT NULL,
             user_name VARCHAR(50) NOT NULL,
             entity_status status_enum NOT NULL,
             created_by BIGINT NOT NULL,
             created_date TIMESTAMP WITHOUT TIME ZONE,
             updated_by BIGINT NOT NULL,
             updated_date TIMESTAMP WITHOUT TIME ZONE,
             PRIMARY KEY (id)
);

DROP TABLE IF EXISTS app_access_tokens CASCADE;

CREATE TABLE app_access_tokens(
             id BIGSERIAL NOT NULL,
             refresh_token_id BIGINT NOT NULL,
             token TEXT NOT NULL,
             PRIMARY KEY (id)
             
);

DROP TABLE IF EXISTS app_refresh_tokens CASCADE;

CREATE TABLE app_refresh_tokens(
             id BIGSERIAL NOT NULL,
             app_client_id BIGINT NOT NULL,
             user_name VARCHAR(50) NOT NULL,
             token TEXT NOT NULL,
             PRIMARY KEY (id),
             UNIQUE (app_client_id, user_name)
);


      
ALTER TABLE app_clients_scopes
  ADD CONSTRAINT fk_clients_scopes_app_clients FOREIGN KEY (app_client_id)
      REFERENCES app_clients(id);
     
 ALTER TABLE app_client_users
   ADD CONSTRAINT fk_client_users_users FOREIGN KEY (user_name)
       REFERENCES users(user_name);
 
ALTER TABLE app_client_users
  ADD CONSTRAINT fk_client_users_app_clients FOREIGN KEY (app_client_id)
      REFERENCES app_clients(id);

ALTER TABLE app_refresh_tokens
  ADD CONSTRAINT fk_refresh_tokens_users FOREIGN KEY (user_name)
      REFERENCES users(user_name);
  
ALTER TABLE app_refresh_tokens
   ADD CONSTRAINT fk_refresh_tokens_app_clients FOREIGN KEY (app_client_id)
       REFERENCES app_clients(id);

ALTER TABLE app_access_tokens
  ADD CONSTRAINT fk_access_token_refresh_token FOREIGN KEY (refresh_token_id)
      REFERENCES app_refresh_tokenS(id);

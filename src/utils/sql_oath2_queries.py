# queries to get data from db

SQL_QUERY_TO_GET_USER_BY_USERNAME = """
SELECT *
  FROM users
 WHERE username = :username
   AND entity_status = 'ACTIVE'
"""

SQL_QUERY_TO_GET_CLIENT_BY_CLIENT_ID = """
SELECT *
  FROM app_clients
  WHERE client_id = :client_id
  AND entity_status = 'ACTIVE' 
"""
SQL_QUERY_TO_GET_CLIENT_BY_ID = """
SELECT *
  FROM app_clients
  WHERE id = :id
  AND entity_status = 'ACTIVE'
"""

SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_TOKEN = """
SELECT *
  FROM app_refresh_tokens
  where token = :token
"""

SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_ACCESS_REFRESH_TOKEN_AND_CLIENT = """
SELECT aprt.*
  FROM app_refresh_tokens aprt 
 INNER JOIN app_access_tokens apat 
    ON aprt.id = apat.refresh_token_id
 INNER JOIN app_clients apcl
    ON apcl.id = aprt.app_client_id
 WHERE aprt.token = :refresh_token 
   AND apat.token = :access_token
   AND apcl.client_id = :client_id
   AND apcl.entity_status = 'ACTIVE'
   AND ((EXISTS(SELECT username 
                  FROM app_client_users apcu  
                 WHERE apcu.username = :username
                   AND apcu.entity_status = 'ACTIVE')) 
   OR (char_length(:username) = 0))
"""

SQL_QUERY_TO_GET_SCOPES_BY_CLIENT_ID = """
SELECT scope
 FROM app_clients_scopes
 WHERE app_client_id = :id
"""

SQL_QUERY_TO_GET_CLIENT_USER_BY_USERNAME_AND_CLIENT_ID = """
SELECT *
  FROM app_client_users
  WHERE username = :username 
  AND app_client_id = :app_client_id
  AND entity_status = 'ACTIVE'
"""

# queries to add data to db


SQL_QUERY_TO_ADD_REFRESH_TOKEN = """
INSERT INTO app_refresh_tokens(
  token,
  app_client_id,
  grant_type
)
  
VALUES(
  :token,
  :app_client_id,
  :grant_type
);
"""

SQL_QUERY_TO_ADD_ACCESS_TOKEN = """
INSERT INTO app_access_tokens(
  refresh_token_id,
             token
)

VALUES(
 :refresh_token_id,
 :token
 );
"""
# queries to delete data from db

SQL_QUERY_TO_DELETE_ACCESS_TOKEN_BY_REFRESH_TOKEN_ID = """
DELETE FROM app_access_tokens
where refresh_token_id = :app_refresh_token_id
"""

SQL_QUERY_TO_DELETE_REFRESH_TOKEN = """
DELETE FROM app_refresh_tokens
where token = :token
"""

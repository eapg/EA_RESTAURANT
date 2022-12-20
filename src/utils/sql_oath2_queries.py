# queries to get data from db

SQL_QUERY_TO_GET_USER_BY_USERNAME = """
SELECT *
  FROM users
  where username = :username
"""

SQL_QUERY_TO_GET_CLIENT_BY_CLIENT_ID = """
SELECT *
  FROM app_clients
  WHERE client_id = :client_id
"""
SQL_QUERY_TO_GET_CLIENT_BY_ID = """
SELECT *
  FROM app_clients
  WHERE id = :id
"""

SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_TOKEN = """
SELECT *
  FROM app_refresh_tokens
  where token = :token
"""

SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_ACCESS_AND_REFRESH_TOKEN = """
SELECT art.*
  FROM app_refresh_tokens art 
 INNER JOIN app_access_tokens aat 
    ON art.id = aat.refresh_token_id 
 WHERE art.token = :refresh_token AND aat.token = :access_token
"""

SQL_QUERY_TO_GET_SCOPES_BY_CLIENT_ID = """
SELECT scope
 FROM app_clients_scopes
 WHERE app_client_id = :id
"""

SQL_QUERY_TO_GET_CLIENT_USER_BY_USERNAME_AND_CLIENT_ID = """
SELECT *
  FROM app_client_users
  WHERE username = :username and app_client_id = :app_client_id
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

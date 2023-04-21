import base64


def generate_basic_token_from_credentials(client_id, client_secret):
    credentials = client_id + ':' + client_secret
    basic_token_encode = base64.b64encode(credentials.encode('utf-8'))
    basic_token = 'Basic' + ' ' + basic_token_encode.decode('utf-8')
    return basic_token

import base64
from src.password_encoder.base_encoder import BaseEncoder


class Base64Encoder(BaseEncoder):
    def validate_password(self, password, encoded_password):
        decoded_password = base64.b64decode(encoded_password).decode("utf-8")
        if decoded_password == password:
            return True
        else:
            return False

    def encode_password(self, pass_data):
        return base64.b64encode(pass_data.encode("utf-8")).decode("ascii")


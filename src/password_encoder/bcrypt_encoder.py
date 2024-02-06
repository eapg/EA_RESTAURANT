import bcrypt

from src.password_encoder.base_encoder import BaseEncoder


class BcryptEncoder(BaseEncoder):
    def validate_password(self, password, encoded_password):
        return bcrypt.checkpw(password.encode("utf-8"), encoded_password.encode("utf-8"))

    def encode_password(self, pass_data):
        password_bytes = pass_data.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password_bytes, salt)
        decode_hash_password = hash_password.decode("utf-8")
        return decode_hash_password

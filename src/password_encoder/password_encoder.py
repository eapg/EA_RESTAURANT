from injector import Module


class PasswordEncoder(Module):

    def __init__(self, password_encoder):
        self.password_encoder = password_encoder

    def validate_password(self, password, encoded_password):
        return self.password_encoder.validate_password(password, encoded_password)

    def encode_password(self, pass_data):
        return self.password_encoder.encode_password(pass_data)

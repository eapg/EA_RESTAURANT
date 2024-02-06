from src.constants.password_encoder import PasswordEncoderType
from src.env_config import get_env_config_instance
from src.password_encoder.base64_encoder import Base64Encoder
from src.password_encoder.bcrypt_encoder import BcryptEncoder
from src.password_encoder.password_encoder import PasswordEncoder


def get_password_encoder():
    env_config = get_env_config_instance()

    if env_config.password_encoding_type == PasswordEncoderType.BASE64.value:
        return PasswordEncoder(Base64Encoder())
    elif env_config.password_encoding_type == PasswordEncoderType.BCRYPT.value:
        return PasswordEncoder(BcryptEncoder())

from abc import ABCMeta, abstractmethod


class BaseEncoder(metaclass=ABCMeta):
    @abstractmethod
    def validate_password(self, password, encoded_password):
        pass

    @abstractmethod
    def encode_password(self, pass_data):
        pass

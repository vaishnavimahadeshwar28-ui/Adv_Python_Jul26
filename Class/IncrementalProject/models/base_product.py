from abc import ABC, abstractmethod
from models.metaclass import ProductMeta


class BaseProduct(ABC, metaclass=ProductMeta):

    @abstractmethod
    def display_details(self):
        pass

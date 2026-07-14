from models.base_product import BaseProduct
from models.descriptors import PositiveNumber
from models.descriptors import NonEmptyString


class Product(BaseProduct):

    name = NonEmptyString()
    price = PositiveNumber()
    quantity = PositiveNumber()

    def __init__(self, name, price, quantity):

        self.name = name
        self.price = price
        self.quantity = quantity

    def display_details(self):

        print(f"""
Name      : {self.name}
Price     : {self.price}
Quantity  : {self.quantity}
""")

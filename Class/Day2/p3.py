# Descriptors
# Descriptor is like a security guard, but for your class attributes
class PositiveNumber:
    """
        A descriptor which ensures the value is a positive number
    """
    def __set_name__(self,owner,name):
        self.name = name

    def __get__(self,obj,objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name,None)
    
    def __set__(self,obj,value):
        if value <= 0:
            raise ValueError(f"{self.name} must be positive")
        
        obj.__dict__[self.name] = value

    def __delete__(self,obj):
        del obj.__dict__[self.name]

class Product:
    price = PositiveNumber()
    stock = PositiveNumber()

    def __init__(self,name,price,stock):
        self.name = name

        self.price = price
        self.stock = stock

product = Product("Laptop",50000,10)
# print(product.price)

try:
    product.stock = -50
except ValueError as e:
    print(f"Error: {e}")
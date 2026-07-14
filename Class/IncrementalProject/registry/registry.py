class ProductRegistry:
    """
    Stores all registered product classes.
    """

    _products = {}

    @classmethod
    def register(cls, product_class):
        cls._products[product_class.__name__] = product_class

    @classmethod
    def display_registered_products(cls):
        print("\nRegistered Product Types")
        print("-" * 30)

        for name in cls._products:
            print(name)
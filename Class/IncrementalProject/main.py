from models.product import Product
from registry.registry import ProductRegistry

# Create products
laptop = Product("Laptop", 55000, 10)
mouse = Product("Wireless Mouse", 1200, 50)
keyboard = Product("Mechanical Keyboard", 4500, 25)

print("\nProduct Details")
print("-" * 40)

laptop.display_details()
mouse.display_details()
keyboard.display_details()

# Display automatically registered product classes
ProductRegistry.display_registered_products()
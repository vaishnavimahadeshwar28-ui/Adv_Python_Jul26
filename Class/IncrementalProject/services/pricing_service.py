"""
All the pricing related operations
"""

from functools import wraps

# Decorator 1
def audit(func):
    # Print messages before and after function execution
    @wraps(func)
    # wrapper is a function that replaces the original one when the decorator is used
    def wrapper(*args,**kwargs):
        print("\nCalculating price...")
        result = func(*args,**kwargs)

        print("\nCalculation completed")
        return result
    # The decorator returns the wrapper function, which will be called instead of func
    return wrapper

# Decorator 2
def discount(percent):
    def decorator(func):
        @wraps(func)
        def wrapper(product):
            # Applying the discount to the product's price
            discounted_price = product.price * (1 - percent/100)
            # Call the original function with the product & the new discounted_price
            return func(product,discounted_price)
        return wrapper
    return decorator

# closure
def tax_calculator(rate):
    def calculate(price):
        
        return price * rate / 100
    return calculate

# Create a GST calculator
# gst is a function that calculates 18% tax
gst = tax_calculator(18)

# Main Pricing function
# @audit wraps calculate_price
# @discount(10)

@audit
@discount(10)
def calculate_price(product,discouned_price):
    tax = gst(discouned_price)

    final_price = discouned_price + tax

    return {
        "original": product.price,
        "discounted": discouned_price,
        "tax": tax,
        "final": final_price,
    }

def calculate_prices(products):
    return list(map(calculate_price,products))
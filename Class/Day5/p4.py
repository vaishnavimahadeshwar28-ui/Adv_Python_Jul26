# Decorators
def simple_decorator(func):
    def wrapper():
        print("Before the function call")
        func()
        print("After the function call")

    return wrapper

def say_hello():
    print("Hello world")
# Apply the decorator
decorated_hello = simple_decorator(say_hello)
decorated_hello()

@simple_decorator #say_hi = simple_decorator(say_hi)
def say_hi():
    print("Hi there, Welcome")
say_hi()
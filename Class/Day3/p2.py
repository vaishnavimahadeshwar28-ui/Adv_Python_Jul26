# First-Class Functions

# 1. Assigning a function to a variable
def say_hello(name):
    return f"Hello, {name}!"
# Assign the function to a variable (without parantheses)
greet_function = say_hello

print(greet_function("Vaishnavi"))
print(say_hello("Vaishnavi"))

#2 Passing functions as args
def apply_operation(func,value):
    return func(value)

def double(x):
    return x * 2
# passing different function as argument
print(apply_operation(double,5))

#3 Returning function from function
def make_multiplier(factor):
    def multiplier(x):
        return x*factor
    return multiplier

double = make_multiplier(20)
print(double(2))

#4. Storing function in data structure
operations = {
    'add': lambda x,y: x+y,
    'subtract': lambda x,y: x-y,
}
print(operations['add'](10,5))
print(operations['subtract'](10,5))
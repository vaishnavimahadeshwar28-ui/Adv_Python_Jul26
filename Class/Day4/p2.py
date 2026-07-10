# Higher-order function: Functions that either take other functions as 
# arguments or return functions as results
def apply_twice(func,value):
    return func(func(value))

def add_two(x):
    return x+2

print(apply_twice(add_two,10))

#2. return a function
def make_logger(prefix):
    def logger(message):
        print(f"[{prefix}] {message}")
    return logger

info_logger = make_logger("INFO")
info_logger("System Started")
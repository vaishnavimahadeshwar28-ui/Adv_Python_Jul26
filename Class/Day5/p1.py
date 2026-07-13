# Closure
def outer_function(message):
    captured_message = message

    def inner_function():
        print(f"The message is: {captured_message}")
    return inner_function

hello_closure = outer_function("Hello, world")
close_closure = outer_function("Goodbye, world")

hello_closure()
close_closure()
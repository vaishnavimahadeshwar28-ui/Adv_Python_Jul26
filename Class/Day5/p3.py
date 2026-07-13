# closure vs class
def make_counter():
    count = 0
    def increment():
        # keyword used inside nested function to declare that a variable 
        # belongs to nearest enclosing function scope
        nonlocal count
        count+=1
        return count
    return increment
counter = make_counter()
print(counter())
print(counter())

# Class
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.count
counter_obj = Counter()

print(counter_obj.increment())
print(counter_obj.increment())

# Closure: simple case, single function behaviour
# classes: Complex behaviour with multilple methods
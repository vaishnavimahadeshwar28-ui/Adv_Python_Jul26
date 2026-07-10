# Impure function: has sideeffects modifies external state
counter = 0
def impure_increment():
    global counter
    counter += 1
    return counter

# print(impure_increment())
# print(impure_increment())

def pure_increment(x):
    return x+1

print(pure_increment(5))
print(pure_increment(5))
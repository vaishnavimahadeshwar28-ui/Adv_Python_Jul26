# Components of closure
# 1 The outer function
# 2 The inner function
# 3 The returned inner function
def multiplier(factor):
    def multiply_by_factor(x):
        return x*factor
    return multiply_by_factor

double = multiplier(2)
triple = multiplier(3)

#print(double(10))
#print(triple(20))

print(double.__closure__)
print(double.__closure__[0].cell_contents)
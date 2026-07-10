# Immutability

# Mutable
my_list = [1,2,3]
my_list[0] = 10
# print(my_list)

# Immutable
my_tuple = (1,2,3)
# my_tuple[0] = 10

def pure_process(data):
    return data + (4,5,6)

original = (1,2,3)
processed = pure_process(original)

print(original)
print(processed)
fruits = ['apple','banana','cherry']
# for fruit in fruits:
#     print(fruit)
iterator = iter(fruits)
while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
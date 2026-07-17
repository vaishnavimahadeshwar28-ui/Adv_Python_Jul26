# Loops: allows us iterate over collection of items
# Basic for loop
fruits = ['apple','banana','cherry']
for fruit in fruits:
    print(fruit)

# for loop with range
for i in range(5):
    print(i)

# for loop with dictionary
person = {'name':'Vaishnavi','age':19,'city':'Mumbai'}
for key,value in person.items():
    print(f"{key}:{value}")
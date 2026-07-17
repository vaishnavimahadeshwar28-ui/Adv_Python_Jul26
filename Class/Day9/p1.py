# functions & Classes
def greet(name):
    return f"Hello, {name}"
class Dog:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def bark(self):
        return f"{self.name} says woof"
    
print(greet("Vaishnavi"))
my_dog = Dog("Leo",5)
print(my_dog.bark())
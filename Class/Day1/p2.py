#Parent class / base class
class Animal:
    def __init__(self,name):
        self.name=name
    
    def makeSound(self):
        return "Some sound"
    
#Child class / derived class
class Cat(Animal):
    def makeSound(self):
        return f"{self.name} says meow"
    
#Child class / derived class
class Cow(Animal):
    def makeSound(self):
        return f"{self.name} says moo"
    
cat=Cat("Tom")
cow=Cow("Radha")

print(cat.makeSound())
print(cow.makeSound())
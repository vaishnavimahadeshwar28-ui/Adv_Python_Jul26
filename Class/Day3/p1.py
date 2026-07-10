# If a class is a blueprint for creating objects, then a metaclass is a blueprint for creating 
# classes

import datetime
class SimpleMeta(type):
    def __new__(cls,name,bases,attrs):
        print(f"Creating classes: {name}")
        print(f"Base classes: {bases}")
        print(f"Attributes:{list(attrs.keys())}")

        attrs['created_at'] = datetime.datetime.now()
        attrs['created_by'] = 'SimpleMeta'

        return super().__new__(cls,name,bases,attrs)
    
class MyClass(metaclass=SimpleMeta):
    x = 10

    def method(self):
        return "Hello"

print(MyClass.x)
print(MyClass.created_at)
print(MyClass.created_by)
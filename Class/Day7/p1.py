# Iterator vs Iterable
# Iterable: can be iterated over (has __iter__)
# Iterable: A collection you can loop over: list,tuple,dictionary
# Iterator: Keeps state and produces values (has __iter__ and __next__)
# Iterator: The object that actually gives one item at a time
# Book is iterable
# Iterator: turning pages one after the other

from collections.abc import Iterable, Iterator
# Lists are iterable, not iterators
my_list = [1,2,3]
print(isinstance(my_list,Iterable))
print(isinstance(my_list,Iterator))

class MyIterable:
    def __init__(self,data):
        self.data = data

    def __iter__(self):
        return MyIterator(self.data)
    
class MyIterator:
    def __init__(self,data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        
        value = self.data[self.index]
        self.index +=1
        return value
    
iterable = MyIterable([1,2,3,4])

print(list(iterable))
print(list(iterable)) #new iterator instance gets created
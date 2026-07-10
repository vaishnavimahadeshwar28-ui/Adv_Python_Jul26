#Dunder methods : Double Underscore
class Book:
    def __init__(self,title,author):
        self.title=title
        self.author=author
    #String representation for users
    def __str__(self):
        return f"{self.title} by {self.author}"
    #String represenations for developers
    def __repr__(self):
        return f"Book('{self.title}','{self.author}')"
    #Euality comparison
    def __eq__(self,other):
        if not isinstance(other,Book):
            return False
        return self.title== other.title and self.author==other.author
    
book1=Book("Python 101","Mark Davis")
book2=Book("Python 101","Mark Davis")
book3=Book("Advanced Python","Tom Harry")

print(book1)
print(repr(book1))
print(book1 == book2)
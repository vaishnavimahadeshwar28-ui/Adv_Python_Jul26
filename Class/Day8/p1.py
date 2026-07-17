# Generator
def squares(n):
    for i in range(1,n+1):
        yield i**2

sq = squares(5) 
print(next(sq)) #1
print(next(sq)) #4
print(next(sq)) #9
print(next(sq)) #16
print(next(sq)) #25
#print(next(sq)) #error
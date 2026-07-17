def simple_generator():
    print("Step1: 1st yield")
    yield 1

    print("Step2: 2nd yield")
    yield 2

    print("Step3: 3rd yield")
    yield 3

    print("Generator is done")

gen = simple_generator()

print(next(gen)) #1
print(next(gen)) #2
print(next(gen)) #3
# print(next(gen)) #error
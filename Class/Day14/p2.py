# File Handling:read from or write to file.
with open('sample.txt','r') as file:
    content = file.read()
    # print("Entire file:")
    # print(content)

with open('sample.txt','r') as file:
    chunk = file.read(10)
    # print(f"First 10 chars: {chunk}")

# readline()
with open('sample.txt','r') as file:
    line1 = file.readline()
    line2 = file.readline()
    # print(f"Line 1: {line1.strip()}")
    # print(f"Line 2: {line2.strip()}")

#readlines(): reads all the lines into a list
with open('sample.txt','r') as file:
    lines = file.readlines()
    # print(lines)

# Iterating line by line
with open('sample.txt','r') as file:
    for line in file:
        print(line.strip())
# File Handling: reading & writing to files on computer
# Writing to a file
with open('example.txt','w')as file:
    file.write('Hello, World')

# Reading from a file
with open('example.txt','r')as file:
    content = file.read()
    print(content)

# Reading line by line
with open('example.txt','r')as file:
    for line in file:
        print(line.strip())
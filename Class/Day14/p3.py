# Writing to files
# 1. write()
with open('output.txt','w') as file:
    file.write("India, officially the Republic of India, is a country in South Asia.")
    file.write("It is the world's seventh-largest country by area and the largest by population.[20] ")

# 2. writelines()
with open('output2.txt','w') as file:
    lines = ["Line 1\n","Line 2\n", "Line 3\n"]
    file.writelines(lines)

# 3 write with formatting
name = "Rakesh"
age = 30
with open('formatted.txt','w') as file:
    file.write(f"Name: {name}\n")
    file.write(f"Age: {age}\n")
    file.write("Name: {}\nAge: {}\n".format(name,age))

# 4 appending to file
with open('formatted.txt','a') as file:
    file.write("This line is appended")
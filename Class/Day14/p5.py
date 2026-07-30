import csv
data = [
    ['Name','Age',"City"],
    ['Vaishnavi',19,"Mumabi"],
    ['Sonia',19,"Mumbai"],
    ['Ana',19,"Mumbai"]
]

with open('people.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# Using DictWriter
data_dicts = [
    {'Name':'Vaishnavi','Age':'19','City':'Mumbai'},
    {'Name':'Sonia','Age':'19','City':'Mumbai'}
] 
with open('people_dict.csv','w',newline='') as file:
    filenames = ['Name','Age','City']
    writer = csv.DictWriter(file, fieldnames=filenames)
    writer.writeheader()
    writer.writerows(data_dicts)

# Read from csv
# 1. using reader
with open('people.csv','r') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

# 2 using DictReader
with open('people_dict.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"{row['Name']} is {row['Age']} from {row['City']}")
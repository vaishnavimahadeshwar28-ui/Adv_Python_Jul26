# Data Serialization:
# converting complex datastructure into a format that can be store or transmitted easily
# reverse of it is De-Serialization

import json
# (Json: JavaScript Object Notation)
data = {
  "firstName": "John",
  "lastName": "Doe",
  "age": 30,
  "isEmployed": True,
  "hobbies": ["reading", "traveling", "swimming"],
  "address": {
    "street": "123 Main Street",
    "city": "New York",
    "zipCode": "10001"
  }
}

# Serialize to JSON string
json_string = json.dumps(data)
print("JSON string:")
print(json_string)

# De-Serialize from JSON string
parsed_data = json.loads(json_string)
print("Parsed data:")
print(parsed_data)

# Write to file
with open('data.json','w') as file:
    json.dump(data, file, indent=2)

# Read from file
with open('data.json','r') as file:
    loaded_data = json.load(file)
    print("loaded from file:")
    print(loaded_data)
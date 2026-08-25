# Pickle: Py's native seriazation format; use it with any Python Object
import pickle
# Py Obj
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
  },
  'scores': (85,99,24), #Tuple
  'set_data': {1,2,3},

}
# Serialze to bytes
pickeled_bytes = pickle.dumps(data)
print("Pickled string:")
print(pickeled_bytes)
# De-Serialze to bytes
unpickeled_bytes = pickle.loads(pickeled_bytes)
print("upPickled data:")
print(unpickeled_bytes)

print(f"Type preserved: {type(unpickeled_bytes['scores'])}")
print(f"Type preserved: {type(unpickeled_bytes['set_data'])}")

# write to file
with open('data.pickle','wb') as file:
    pickle.dump(data, file)

# Read from file
with open('data.pickle','rb') as file:
    loaded_data = pickle.load(file)
    print("loaded from pickle file:")
    print(loaded_data)
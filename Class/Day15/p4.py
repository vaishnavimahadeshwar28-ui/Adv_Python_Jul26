# Groups & Capturing
import re

pattern = r"(\d{3})-(\d{3})-(\d{4})"
text = "call 996-473-1234"
match = re.search(pattern,text)
print(match.group(0))
print(match.group(1))
print(match.group(2))
print(match.group(3))
print(match.group())

# named groups
pattern = r"(?P<area>\d{3})-(?P<exchange>\d{3})-(?P<number>\d{4})"
match = re.search(pattern,text)
print(match.group('area'))
print(match.group('exchange'))
print(match.group('number'))

# Non-capturing groups
pattern = r"(?:\d{3})-\d{3}-\d{4}" # doesn't recognize/capture the first group
text = "Phone: 996-473-1234"
match = re.search(pattern,text)
print(match.groups())

# Back references
pattern = r"(\w+)\s+\1" # word repeated twice
text = " hello hello hello"
match = re.search(pattern,text)
print(match.group())
# Anchors and Boundaries
import re

# ^ : start of string
pattern = r"^Hello"
text = "Hello World"
matches = re.search(pattern,text)
print(matches)

# $ : end of string
pattern = r"Hello$"
text = "Hello World"
matches = re.search(pattern,text)
print(matches)

# \b : word boundary
pattern = r"\bword\b"
text = "word words wordy"
matches = re.findall(pattern,text)
print(matches)
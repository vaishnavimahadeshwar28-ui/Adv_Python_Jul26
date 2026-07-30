import re
# Literal characters
pattern = "hello"
text = "hello world"

match = re.search(pattern, text)
print(match)

# Special characters
pattern = "h.llo" # hello | h1llo | h@llo
text = "hello world"

match = re.search(pattern, text)
print(match)

# \d - Any digit (0-9)
# 123-456-7890
pattern = r"\d{3}-\d{3}-\d{4}"
text = "call 996-473-1234 now"
match = re.search(pattern,text)
print(match.group())

# \w - Any word character (a-z, A-Z, 0-9, _)
pattern = r"\w+" 
text = "Hello_123"
match = re.search(pattern,text)
print(match.group())

# \s - Any whitespaces (space, tab, newline)
pattern = r"\s" 
text = "Hello World"

match = re.search(pattern, text)
print(match)

#  [] character class
pattern = f"[aeiou]"
text = "hello"
matches = re.findall(pattern,text)
print(matches)

# ^ negated character class
pattern = f"[^aeiou]"
text = "hello"
matches = re.findall(pattern,text)
print(matches)
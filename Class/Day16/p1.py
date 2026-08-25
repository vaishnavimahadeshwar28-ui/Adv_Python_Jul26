# common Regex functions
import re
text = "Hello world! This is a test. Phone: 123-456-7890. Email:r@r.com"
# re.search()
# pattern = r"\d{3}-\d{3}-\d{4}"
# # text = "call 996-473-1234 now"
# match = re.search(pattern,text)
# print(match.group())
match = re.search(r"\d{3}-\d{3}-\d{4}",text)
# re.finditer() - find all matches as iterators
for match in re.finditer(r"\w+",text):
    print(f"Word: {match.group()} at position {match.start()}-{match.end()}")

# re.sub() - Replace matches
cleaned = re.sub(r"\d{3}-\d{3}-\d{4}","XXX-XXX-XXXX",text)
print(cleaned)

# re.split() - split by pattern
words = re.split(r"\s+",text)
print(words)
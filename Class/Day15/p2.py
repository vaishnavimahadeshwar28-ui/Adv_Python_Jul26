# Quatifiers
import re 
pattern = r"ab*"
text = "a ab abb abbb"
matches = re.findall(pattern,text)
print(matches)

# 1 or more
pattern = r"ab+"
text = "a ab abb abbb"
matches = re.findall(pattern,text)
print(matches)

# 0 or 1
pattern = r"ab?"
text = "a ab abb abbb"
matches = re.findall(pattern,text)
print(matches)

# {n} exactly n
pattern = f"a{3}"  # 3 chars
text = "aa aaa aaaa"
matches = re.findall(pattern,text)
print(matches)

# {n,} at least n
pattern = r"a{2,}"
text = "a aa aaa aaaa"
matches = re.findall(pattern,text)
print(matches)

# {n,m}: between n and m
pattern = "a{2,3}"

text = "a aa aaa aaaa"
matches = re.findall(pattern,text)
print(matches)
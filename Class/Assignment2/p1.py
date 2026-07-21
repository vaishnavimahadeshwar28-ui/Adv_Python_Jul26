def count_characters(text):
    d={}

    text=text.lower()
    for ch in text:
        if ch.isalpha():
            if ch in d:
                d[ch] += 1
            else:
                d[ch] = 1

    result={}

    for student in sorted(d):
        result[student] = d[student]
    return result

text=input("Enter string: ")
print(count_characters(text))
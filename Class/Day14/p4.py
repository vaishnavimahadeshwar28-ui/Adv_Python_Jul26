# Working with file positions
with open('sample.txt','rb') as file:
    # Get current position
    position = file.tell()
    print(f"Current Position: {position}")

    # Read 15 bytes
    content = file.read(15)
    print(f"Read : {content}")

    # Get new position
    position = file.tell()
    print(f"Current Position: {position}")

    # Seek
    file.seek(2)
    print(f"Moved to position: {file.tell()}")

    # Read from there
    content = file.read(4)
    print(f"Read from position 2:{content}")

    # seek from current position
    file.seek(2,1)
    content = file.read(3)
    print(f"Read after moving 2 from current:{content}")

    # seek from end position
    file.seek(-1,2)
    content = file.read(2)
    print(f"Read from 3 from current:{content}")
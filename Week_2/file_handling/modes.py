# 1. 'r' – Read-Only Mode
#    Use it when you want to read an existing file.
#    Will throw FileNotFoundError if file doesn’t exist.

with open("content.txt", "r") as f:
    for line in f:
        print(line.strip())


# 2. 'w' – Write Mode
#    Use it to write to a file.
#    If file exists, it gets overwritten (truncated to 0 bytes).
#    Creates file if it doesn't exist.

students = ["Alice", "Bob", "Charlie"]

with open("students.txt", "w") as f:
    for student in students:
        f.write(student + "\n")


# 3. 'a' – Append Mode
#    Use it to add content to the end of a file.
#    Doesn’t erase existing data.
#    Creates the file if it doesn’t exist.

with open("example.txt", "a") as f:
    f.write("\nNew Line Added!")


# 4. 'x' – Exclusive Creation Mode
#    Use when you want to create a new file.
#    Throws FileExistsError if the file already exists.

try:
    with open("example.txt", "x") as f:
        f.write("Created new file!")
except FileExistsError:
    print("File already exists!")


# 5. 'r+' – Read & Write Mode (No Truncate)
#     Allows you to read and write both.
#     File must exist.
#     Doesn’t erase content (you must manually overwrite or seek).


with open("example.txt", "r+") as f:
    content = f.read()
    f.seek(0)
    f.write("Overwritten!")  # Overwrites from start


# 6. 'a+' – Append & Read Mode
#    Can read and write
#    Writes are always appended at the end
#    File is created if not present
#    Doesn’t truncate


with open("example.txt", "a+") as f:
    f.write("\nNew appended line")
    f.seek(0)  # Need to rewind to read
    print(f.read())

# 7. 'w+' – Write & Read Mode (Truncates)
#    Allows read and write
#    Creates the file if not exists
#    Truncates the file to zero bytes if it exists

with open("example.txt", "w+") as f:
    f.write("Fresh content")
    f.seek(0)
    print(f.read())


# Working with Binary Files
# Mode	 Use Case
# 'rb' - Read a binary file (e.g., image, audio)
# 'wb' - Write binary data
# 'ab' - Append binary data


# Read an image
with open("photo.jpeg", "rb") as f:
    data = f.read()

# Write a binary file
with open("backup.bin", "wb") as f:
    f.write(b"Binary data here")

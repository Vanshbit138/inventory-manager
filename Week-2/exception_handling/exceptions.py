# 🔸 1. What is an Exception?
# An exception is a runtime error that disrupts the normal flow of your Python program. 
# For example, dividing by zero or trying to open a file that doesn’t exist.


# 🔸 2. Why Handle Exceptions?
# Without handling exceptions:

# Your program crashes

# Users see ugly error messages

# You can't control error flow

# Instead, use try...except to gracefully handle these situations.

# try:
#     with open("data.txt") as f:
#         print(f.read())
# except FileNotFoundError:
#     print("File does not exist.")



# try:
#     num = int(input("Enter number: "))
#     print(100 / num)
# except ValueError:
#     print("That's not a valid number.")
# except ZeroDivisionError:
#     print("Cannot divide by zero.")


def process_numbers(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            print(type(lines))
            for i, line in enumerate(lines, start=1):
                line = line.strip()
                
                if not line:
                    print(f"Line {i}: Skipping empty line")
                    continue

                try:
                    number = int(line)
                    result = 100 / number
                    print(f"Line {i}: 100 / {number} = {result}")
                except ValueError:
                    print(f"Line {i}: Cannot convert '{line}' to integer")
                except ZeroDivisionError:
                    print(f"Line {i}: Cannot divide by zero")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run it
process_numbers("numbers.txt")


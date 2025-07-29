"""
data_types_demo.py

Demonstrates Python's basic data types, variable assignments,
and string formatting using f-strings.
"""

def describe_person(name: str, age: int, height: float, is_student: bool) -> str:
    """
    Returns a formatted string describing a person.

    Args:
        name (str): The person's name.
        age (int): The person's age in years.
        height (float): The person's height in feet.
        is_student (bool): True if the person is a student.

    Returns:
        str: A description of the person.
    """
    student_status = "a student" if is_student else "not a student"
    return f"{name} is {age} years old, {height} feet tall, and is {student_status}."


# Sample usage
if __name__ == "__main__":
    description = describe_person("Vansh", 23, 5.8, True)
    print(description)


# Arithmetic examples
x = 10
y = 3
sum_ = x + y       # 13
product = x * y    # 30
quotient = x / y   # 3.333...
modulus = x % y    # 1


# Comparison
print("***Comparison Operators***")
print(x == y)   # False
print(x != y)   # True
print(x > y)    # True


#Logical Operators
print("***Logical Operators***")
a = True
b = False
print(a and b)  # False
print(a or b)   # True
print(not a)    # False

#Equality Vs. Identity Operators
print("***Equality Vs. Identity Operators***")
x = [1, 2]
y = [1, 2]

print(x == y)  # True (values are equal)
print(x is y)  # False (different objects in memory)


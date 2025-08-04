# Using For Loop:
squares = []
for i in range(5):
    squares.append(i * i)
print(squares)  # [0, 1, 4, 9, 16]


# Pythonic Version:
squares = [i * i for i in range(5)]
print(squares)  # [0, 1, 4, 9, 16]


"""
pythonic_demo.py

Demonstrates Pythonic coding style with list comprehensions,
equality vs identity, and Zen of Python principles.
"""


def get_even_numbers(numbers: list[int]) -> list[int]:
    """
    Filters even numbers from a list using list comprehension.

    Args:
        numbers (list[int]): The list of integers.

    Returns:
        list[int]: A list of even integers.
    """
    return [num for num in numbers if num % 2 == 0]


def compare_values():
    """
    Demonstrates the difference between equality (==) and identity (is).
    """
    a = [1, 2, 3]
    b = [1, 2, 3]

    print("a == b:", a == b)  # True – values are equal
    print("a is b:", a is b)  # False – different objects in memory


if __name__ == "__main__":
    evens = get_even_numbers([1, 2, 3, 4, 5, 6])
    print("Even numbers:", evens)

    compare_values()

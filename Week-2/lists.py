def demonstrate_list_properties():
    """
    Demonstrates the creation and basic characteristics of a list in Python.
    Lists are:
    - Mutable sequences enclosed in square brackets []
    - Can hold heterogeneous data types
    - Support indexing and slicing
    """
    my_list = [1, 2, 3.121, "Bharat", True, False, 2+6j, [1, 2, 3, 4], [5, 6, 6, 1]]
    print(type(my_list))
    print(my_list)


def demonstrate_list_functions():
    """
    Demonstrates usage of common list methods like append(), insert(), and clear().
    """
    list1 = [1, 2, 3, 4, 5, 6, 7, 9]
    list1.append(5)
    print("After append:", list1)

    list1.insert(4, 4.5)
    print("After insert:", list1)

    # Uncomment below line to clear list
    # list1.clear()


def count_elements():
    """
    Counts the number of elements in a list using a loop.
    """
    list_ = [1, 2, 3, 4, 4.5, 4.5, 5, 6, 7, 9, 5]
    count = 0
    for i in list_:
        count += 1
    print("Total elements:", count)


def fizz_buzz_logic():
    """
    Applies FizzBuzz logic to numbers 1 through 15:
    - Multiples of 3 -> 'Fizz'
    - Multiples of 5 -> 'Buzz'
    - Multiples of both -> 'FizzBuzz'
    """
    list_ = list(range(1, 16))
    new = []

    for i in list_:
        if i % 3 == 0 and i % 5 == 0:
            new.append("FizzBuzz")
        elif i % 3 == 0:
            new.append("Fizz")
        elif i % 5 == 0:
            new.append("Buzz")
        else:
            new.append(i)

    print("FizzBuzz Output:", new)


def demonstrate_list_comprehension():
    """
    Shows examples of list comprehension:
    - Squaring numbers from 1 to 10
    - Filtering even numbers from 1 to 20
    """
    squares = [i ** 2 for i in range(1, 11)]
    print("Squares:", squares)

    evens = [i for i in range(1, 21) if i % 2 == 0]
    print("Even numbers:", evens)


if __name__ == "__main__":
    demonstrate_list_properties()
    demonstrate_list_functions()
    count_elements()
    fizz_buzz_logic()
    demonstrate_list_comprehension()

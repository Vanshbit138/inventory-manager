"""
control_flow_and_functions.py

Demonstrates core Python concepts:
- if/elif/else conditionals
- for and while loops
- function creation and usage
- Single Responsibility Principle (SRP)
Each function includes a clear docstring for maintainability.
"""

# Function 1: Greet user based on age
def greet_by_age(age):
    """
    Return a greeting based on the user's age.

    Parameters:
        age (int): Age of the user.

    Returns:
        str: Age-appropriate greeting.
    """
    if age < 13:
        return "Hello, child!"
    elif age < 18:
        return "Hi, teen!"
    else:
        return "Welcome, adult!"

# Function 2: Print each fruit using for loop
def list_fruits(fruits):
    """
    Print each fruit in the given list.

    Parameters:
        fruits (list): List of fruit names.
    """
    print("\nFruit List:")
    for fruit in fruits:
        print("-", fruit)

# Function 3: Count to N using a while loop
def count_to_n(n):
    """
    Count from 1 to n using a while loop.

    Parameters:
        n (int): The number to count up to.
    """
    print("\nCounting to", n)
    count = 1
    while count <= n:
        print(count)
        count += 1

# Function 4: Add two numbers and return the sum
def add_numbers(a, b):
    """
    Add two numbers and return their sum.

    Parameters:
        a (int or float): First number.
        b (int or float): Second number.

    Returns:
        int or float: Sum of a and b.
    """
    return a + b

# Function 5: Check if a number is prime
def is_prime(n):
    """
    Check whether a number is prime.

    Parameters:
        n (int): Number to check.

    Returns:
        bool: True if prime, False otherwise.
    """
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function 6: Print all prime numbers in a range
def print_primes_in_range(start, end):
    """
    Print all prime numbers in the given range.

    Parameters:
        start (int): Starting number of the range.
        end (int): Ending number of the range.
    """
    print(f"\nPrime numbers between {start} and {end}:")
    for num in range(start, end + 1):
        if is_prime(num):
            print(num, end=' ')
    print()  # newline

# Function 7: Save order (Dummy function for SRP)
def save_to_db(order_id):
    """
    Simulate saving an order to the database.

    Parameters:
        order_id (str): The order identifier.
    """
    print(f"\nOrder {order_id} saved to database.")

# Function 8: Send confirmation email (Dummy function for SRP)
def send_confirmation(order_id):
    """
    Simulate sending a confirmation email.

    Parameters:
        order_id (str): The order identifier.
    """
    print(f"Confirmation email sent for order {order_id}.")

# Function 9: Process an order using SRP
def process_order(order_id):
    """
    Process an order by saving it and sending confirmation.

    Parameters:
        order_id (str): The order identifier.
    """
    save_to_db(order_id)
    send_confirmation(order_id)


#      Main Script

if __name__ == "__main__":
    # 1. Greet based on age
    print(greet_by_age(12))
    print(greet_by_age(16))
    print(greet_by_age(25))

    # 2. List of fruits
    fruits = ["apple", "banana", "cherry"]
    list_fruits(fruits)

    # 3. Count to N
    count_to_n(5)

    # 4. Add numbers
    print("\nSum of 10 and 20 is:", add_numbers(10, 20))

    # 5. Check if numbers are prime
    print("\nIs 11 prime?", is_prime(11))
    print("Is 4 prime?", is_prime(4))

    # 6. Prime numbers in a range
    print_primes_in_range(10, 20)

    # 7. Process an order
    process_order("ORD123")

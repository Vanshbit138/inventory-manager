d = {"Key1": 2, "Key2": 3}
print(d)


dict1 = {"Key1": 51, "Key2": 52, "key3": 53}

print(dict1)
print(type(dict1))

# Dictionary Functions

d1 = ["a", "b", "c"]
s = dict.fromkeys(d1, 0)
print(s)


d = {"a": 0, "b": 0, "c": 0}
d.pop("a")
print(d)


d = {"a": 0, "b": 0, "c": 0}
c = d.popitem()
print(c)


# Creating a dictionary
student = {"name": "Vansh", "age": 21, "courses": ["Math", "Python"]}

# Accessing values
print(student["name"])  # Output: Vansh
print(student.get("age"))  # Output: 21
print(student.get("grade", "N/A"))  # Output: N/A (default if key doesn't exist)

# Adding or updating key-value pairs
student["age"] = 22
student["grade"] = "A"

# Removing a key
student.pop("courses")

# Iterating
for key, value in student.items():
    print(key, "->", value)



# Set Creation
print("\n--- Set Creation ---")
empty_set = set()
num_set = {1, 2, 3, 4, 5}
dup_set = {1, 2, 2, 3}
print("Duplicate removed set:", dup_set)

# Add / Update
print("\n--- Adding Elements ---")
s = {1, 2}
s.add(3)
s.update([4, 5], {6})
print("After add & update:", s)

# Remove / Discard / Pop / Clear
print("\n--- Removing Elements ---")
s.remove(6)
s.discard(100)  # No error
popped = s.pop()
print("After remove & pop:", s)
print("Popped item:", popped)
s.clear()
print("After clear:", s)

# Set Operations
print("\n--- Set Theory Operations ---")
a = {1, 2, 3}
b = {3, 4, 5}
print("A union B:", a | b)
print("A intersection B:", a & b)
print("A difference B:", a - b)
print("A symmetric difference B:", a ^ b)


# 1. Remove duplicates from list
print("\n--- Real-World: Remove Duplicates ---")
items = [1, 2, 2, 3, 4, 4, 5]
unique_items = list(set(items))
print("Unique items:", unique_items)

# 2. Detect duplicates
print("\n--- Real-World: Detect Duplicates ---")
seen = set()
for item in [1, 2, 3, 2, 4]:
    if item in seen:
        print("Duplicate found:", item)
    seen.add(item)

# 3. Common students
print("\n--- Real-World: Common Students ---")
class_a = {"Alice", "Bob", "Charlie"}
class_b = {"Charlie", "David"}
common = class_a & class_b
print("Common students:", common)

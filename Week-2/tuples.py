# Tuples

tup = (1, 2, 3.124, "String", True, False, 3 + 2j, [1, 2, 3, 4, 5, 6], {"India": 1})

print(tup[-2:-6:-1])

print(tup[-7:-2:-1])

print(tup[::-1])


# Tuple Functions

tuple_ = (1, 2, 3, 4, 5, 6, 6, 6)
x = tuple_.index(5)
print(x)

y = tuple_.count(6)
print(y)


tup = (1, 2, 3, 42, 66, 366, 56)

for i in tup:
    if i == 42:
        print("value presnet in tuple")
        break

# List

# Tuples are another fundamental data structure in Python, serving as ordered collections of elements.
# Detailed Definition:

# List are mutable sequences of items enclosed in square brackets [].
# Once created, you can modify individual elements or the size of the list.
# Elements can be of different data types, creating heterogeneous lists.
# Lists are indexed, starting from 0. .
# Slicing works the same as with tuple to extract sub-lists.





my_list = [1,2,3.121,"Bharat",True,False,2+6j,[1,2,3,4],[5,6,6,1] ]
my_list
print(type(my_list))


#List Functions:

list1 = [1,2,3,4,5,6,7,9]
list1.append(5)
print(list1)            # list1 = [1, 2, 3, 4, 5, 6, 7, 9, 5]


list1.insert(4,4.5)
print(list1)


#list1.clear()

list_ = [1, 2, 3, 4, 4.5, 4.5, 5, 6, 7, 9, 5]
count = 0

for i in list_:
  count +=1
print(count)



list_ = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

new = []
# 3 - > Fizz
# 5 - > Bizz
# 3 & 5 > FizzBuzz


for i in list_:
  if i % 3 == 0 and i % 5 == 0:
    new.append("FizzBuzz")
  elif i % 3 == 0:
    new.append("Fizz")
  elif i % 5 ==0:
    new.append("Buzz")
  else:
    new.append(i)

print(new)


# List Comprihention

new = [i ** 2 for i in range(1,11)]
print(new)


new = [i for i in range(1,21) if i % 2 == 0]
print(new)
#  1. What is the csv module?
# The csv module in Python is part of the standard library that provides functions to read from and write to CSV (Comma-Separated Values) files. A CSV file is simply a text file where each row is a record and fields are separated by commas.

#  2. Why do we need the csv module?
# Real-World Reason:
# Let’s say you’re building a college management system that imports/export student records, attendance, or exam results. These often come from Excel sheets or exported CSVs. Parsing them manually with split(',') is risky because:

# Fields may have commas inside (e.g., "New Delhi, India")

# Fields can be quoted, multiline, or misformatted

# Excel-generated files follow CSV rules


import csv

with open("students.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

#  What is DictReader?
# csv.DictReader reads the first line as keys and returns each row as a dictionary, which is much easier to use in code.


with open("students.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)


# Writing to CSV with csv.writer

data = [
    ["name", "age", "grade"],
    ["Alice", 20, "A"],
    ["Bob", 21, "B"]
]

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)


# Writing to CSV with csv.DictWriter


data = [
    {"name": "Anuj", "age": 20, "grade": "A"},
    {"name": "Raksha", "age": 21, "grade": "B"}
]

with open("output.csv", "w", newline="") as file:
    fieldnames = ["name", "age", "grade"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)


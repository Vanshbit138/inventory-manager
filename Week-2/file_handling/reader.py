import csv


def read_csv_with_reader():
    """
    Reads a CSV file using csv.reader.
    Each row is returned as a list of values.

    Useful for:
    - Simple CSV files without headers
    - Manually handling each column by index
    """
    with open("students.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def read_csv_with_dictreader():
    """
    Reads a CSV file using csv.DictReader.
    The first row is used as keys, and each subsequent row is a dictionary.

    Useful for:
    - Accessing columns by name
    - Cleaner and more readable code
    """
    with open("students.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)


def write_csv_with_writer():
    """
    Writes data to a CSV file using csv.writer.
    Accepts a list of lists where each inner list is a row.

    Useful for:
    - Exporting tabular data without headers
    """
    data = [["name", "age", "grade"], ["Alice", 20, "A"], ["Bob", 21, "B"]]

    with open("output.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def write_csv_with_dictwriter():
    """
    Writes data to a CSV file using csv.DictWriter.
    Accepts a list of dictionaries and writes headers + rows.

    Useful for:
    - Exporting structured data with field names
    - Ensuring consistent column order
    """
    data = [
        {"name": "Anuj", "age": 20, "grade": "A"},
        {"name": "Raksha", "age": 21, "grade": "B"},
    ]

    with open("output.csv", "w", newline="") as file:
        fieldnames = ["name", "age", "grade"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    read_csv_with_reader()
    read_csv_with_dictreader()
    write_csv_with_writer()
    write_csv_with_dictwriter()

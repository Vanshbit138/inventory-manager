# inventory-manager


📁 Root Project Structure

```
inventory-manager/
├── Week-1/                         # Week 1: Git workflow practice
├── Week-2/                         # Week 2: Procedural inventory script
├── Week-3/                         # Week 3: OOP-based inventory manager (not expanded)
│
├── .gitignore                      # Git ignore rules
├── .pre-commit-config.yaml         # Pre-commit hook configuration
├── README.md                       # Project documentation (root-level)
├── setup.cfg                       # Config for formatters/linters (e.g., black, isort)
```

## Week 1 - Git Workflow Tasks

The following tasks were completed as part of Week 1 Git practice:

- [x] Created a **private repository** named `inventory-manager` on GitHub.
- [x] Created and pushed `develop` branch from `main`.
- [x] Created feature branch `feat/week-1` from `develop`.
- [x] Added:
  - `.gitignore` to ignore Python artifacts like `__pycache__`, `*.pyc`, and `venv/`.
  - `README.md` with project description.
  - Simple Python files (`hello.py`, `zen.py`, `datatypes_demo.py`, `pythonic_demo.py`, etc.) for practice.
- [x] Committed changes with meaningful messages to `feat/week-1`.
- [x] Pushed `feat/week-1` to remote.
- [x] Created and handled **Pull Request (PR)** from `feat/week-1` to `develop`.
- [x] Reviewed and merged PR after mentor feedback.

## Scripts Overview

- `hello.py`: Prints a welcome message.
- `zen.py`: Prints "The Zen of Python" for coding philosophy.
- `datatypes_demo.py`: Demonstrates usage of core Python data types.
- `pythonic_demo.py`: Shows Pythonic constructs and best practices.
- `main.py`: Placeholder script (to be extended in later weeks).

## Week 2 - Python Scripting & Error Handling

Structured coding tasks organized by topic to build a CLI-based inventory system.

### 📁 Folder Structure

```
Week-2/
├── data_validation/
│   ├── errors.log
│   ├── inventory.csv
│   ├── low_stock_report.txt
│   └── process_inventory.py
├── exception_handling/
│   ├── exceptions.py
│   └── numbers.txt
├── file_handling/
│   ├── backup.bin
│   ├── content.txt
│   ├── modes.py
│   ├── output.csv
│   ├── photo.jpeg
│   ├── reader.py
│   ├── students.csv
│   └── students.txt
├── conditionals_functions.py
├── dicts.py
├── lists.py
├── sets.py
└── tuples.py
```

### 📌 Topics Covered

✅ **Control structures and reusable functions** (`conditionals_functions.py`)

✅ **Data structures:**
- Lists manipulation and operations (`lists.py`)
- Dictionary operations and methods (`dicts.py`) 
- Set operations and mathematics (`sets.py`)
- Tuple usage and immutability (`tuples.py`)

✅ **File handling** (`file_handling/`)
- Reading and writing text files (`reader.py`, `content.txt`)
- CSV file operations (`students.csv`, `output.csv`)
- Different file modes and binary handling (`modes.py`, `backup.bin`)
- Image file handling (`photo.jpeg`)

✅ **Exception management** (`exception_handling/`)
- Try-catch blocks and error handling (`exceptions.py`)
- Processing numeric data with validation (`numbers.txt`)

✅ **Data validation and processing** (`data_validation/`)
- Inventory data processing (`process_inventory.py`)
- CSV data handling (`inventory.csv`)
- Report generation (`low_stock_report.txt`)
- Error logging (`errors.log`)

### 🧪 Current Git Practice

✅ Created a new branch `feat/week-2` from `develop`

✅ Committed changes for each task logically

✅ Structured folders for modular learning

✅ Pushed changes regularly to `feat/week-2`

✅ Created Pull Request from `feat/week-2` to `develop`

✅ More weeks to follow as the project evolves into a fully functional inventory manager.

## 🛠️ To Run the Project

Make sure you're inside a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt

# Run individual topic scripts
python Week-2/conditionals_functions.py
python Week-2/lists.py
python Week-2/dicts.py
python Week-2/sets.py
python Week-2/tuples.py

# Run file handling examples
python Week-2/file_handling/reader.py
python Week-2/file_handling/modes.py

# Run exception handling examples
python Week-2/exception_handling/exceptions.py

# Run data validation scripts
python Week-2/data_validation/process_inventory.py
```

## Git Commands Practiced

```bash
git clone <repo-url>
git checkout -b develop
git push -u origin develop
git checkout -b feat/week-2
git add .
git commit -m "Add Week-2 Python fundamentals"
git push -u origin feat/week-2
# Create PR from feat/week-2 to develop
```

# Inventory Manager – Week 3

This is a Python-based **Inventory Management System** built using **Object-Oriented Programming (OOP)** principles. It demonstrates clean code structure, data validation, and extendability using inheritance — aligned with industry-standard design principles like **SRP** (Single Responsibility Principle) and **OCP** (Open/Closed Principle).

---

## ✅ Week 3 Goals

- Refactor procedural inventory logic into a structured Python package
- Apply **OOP fundamentals**: class design, encapsulation, and instance methods
- Implement **inheritance** to support different product types
- Follow **SRP**: split responsibilities into focused modules and classes
- Follow **OCP**: extend functionality via subclasses without modifying core logic
- Add **data validation** using `Pydantic v2`
- Generate logs and reports (error log + low stock report)

---

## 📁 Project Structure


```
Week-3/
├── data/
│   └── products.csv               # Sample product data including food, books, etc.
│
├── inventory_manager/
│   ├── __init__.py               # Makes this a Python package
│   ├── core.py                   # Main inventory logic (load, validate, report)
│   ├── models.py                 # Pydantic models (Product base + subclasses)
│   └── utils.py                  # Logging and reporting utilities
│
├── venv/                         # (Optional) Virtual environment for dependencies
│
├── main.py                       # Entry point script to run inventory system│
├── pyproject.toml                # Config for black, ruff, etc.
├── requirements.txt              # Python package dependencies
```
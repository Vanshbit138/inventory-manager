# inventory-manager



##  Week 1 - Git Workflow Tasks

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

##  Scripts Overview

- `hello.py`: Prints a welcome message.
- `zen.py`: Prints "The Zen of Python" for coding philosophy.
- `datatypes_demo.py`: Demonstrates usage of core Python data types.
- `pythonic_demo.py`: Shows Pythonic constructs and best practices.
- `main.py`: Placeholder script (to be extended in later weeks).

## Week 2 - Python Scripting & Error Handling
Structured coding tasks organized by topic to build a CLI-based inventory system.

📁 Folder Structure

Week-2/
├── conditionals_functions.py
├── dicts.py
├── lists.py
├── sets.py
├── tuples.py
├── file_handling/
├── exception_handling/
└── data_validation/
📌 Topics Covered
✅ Control structures and reusable functions

✅ Data structures: lists, dicts, sets, tuples

✅ File reading and writing (file_handling/)

✅ Exception management with try...except (exception_handling/)

✅ Data cleaning and validation with Pydantic (data_validation/)

🧪 Current Git Practice
 Created a new branch feat/week-2 from develop

 Committed changes for each task logically

 Structured folders for modular learning

 Pushed changes regularly to feat/week-2

 Created Pull Request from feat/week-2 to develop

✅ More weeks to follow as the project evolves into a fully functional inventory manager.

🛠️ To Run the Project
Make sure you're inside a virtual environment.

python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python Week-2/main.py     # Or run individual scripts for each concept


##  Git Commands Practiced

```bash
git clone <repo-url>
git checkout -b develop
git push -u origin develop
git checkout -b feat/week-1
git add .
git commit -m "Initial setup"
git push -u origin feat/week-1

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

##  Git Commands Practiced

```bash
git clone <repo-url>
git checkout -b develop
git push -u origin develop
git checkout -b feat/week-1
git add .
git commit -m "Initial setup"
git push -u origin feat/week-1

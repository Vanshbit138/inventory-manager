# Development Journey

This document chronicles the week-by-week development journey of the Inventory Manager project, showcasing the progression from basic Python concepts to a fully-featured application following industry best practices.

##  Learning Objectives

- Master Git workflow and version control
- Progress from procedural to object-oriented programming
- Implement Test-Driven Development (TDD)
- Apply SOLID principles and clean architecture
- Build a production-ready Python application

---

##  Week 1: Git Workflow & Python Fundamentals

**Branch**: `feat/week-1` → `develop`

### Goals Achieved
-  Set up Git workflow with feature branches
-  Established proper project structure
-  Implemented basic Python scripts
-  Configured development tools

### Key Files
```
Week-1/
├── hello.py              # Welcome message
├── zen.py               # Python philosophy
├── datatypes_demo.py    # Core data types
├── pythonic_demo.py     # Python best practices
└── main.py             # Entry point placeholder
```

### Git Workflow Established
```bash
git checkout -b develop
git checkout -b feat/week-1
# Development work
git push -u origin feat/week-1
# Pull Request: feat/week-1 → develop
```

### Skills Demonstrated
- Git branching strategy
- Python syntax and conventions
- Project initialization
- Code organization

---

##  Week 2: Data Structures & File Operations

**Branch**: `feat/week-2` → `develop`

### Goals Achieved
-  Mastered Python data structures
-  Implemented file I/O operations
-  Built error handling mechanisms
-  Created data validation processes

### Project Structure
```
Week-2/
├── data_validation/
│   ├── process_inventory.py    # Core inventory processing
│   ├── inventory.csv          # Sample data
├── exception_handling/
│   ├── exceptions.py          # Error handling patterns
│   └── numbers.txt            # Test data
├── file_handling/
│   ├── reader.py             # File operations
│   ├── modes.py              # File mode examples
│   ├── students.csv          # CSV operations
├── conditionals_functions.py  # Control flow
├── lists.py                  # List operations
├── dicts.py                 # Dictionary methods
├── sets.py                  # Set mathematics
└── tuples.py                # Immutable sequences
```

### Key Achievements
- **Data Structures**: Comprehensive coverage of lists, dicts, sets, tuples
- **File I/O**: Text, CSV, and binary file handling
- **Error Handling**: Try-catch blocks and validation
- **Reporting**: Automated report generation

### Technical Skills
- Exception handling patterns
- CSV data processing
- Logging implementation
- Modular code organization

---

##  Week 3: Object-Oriented Design

**Branch**: `feat/week-3` → `develop`

### Goals Achieved
-  Refactored to Object-Oriented Programming
-  Implemented inheritance hierarchy
-  Applied SOLID principles
-  Added data validation with Pydantic

### Architecture Overview
```
inventory_manager/
├── __init__.py          # Package initialization
├── core.py             # InventoryManager class
├── models.py           # Product hierarchy
└── utils.py            # Utility functions
```

### Class Hierarchy
```python
Product (Base Class)
├── FoodItem
├── ElectronicItem  
└── BookItem
```

### SOLID Principles Applied

**Single Responsibility Principle (SRP)**
- `core.py`: Inventory management logic only
- `models.py`: Data models and validation only
- `utils.py`: Utility functions only

**Open/Closed Principle (OCP)**
- Easy to extend with new product types
- Core logic remains unchanged when adding features

**Liskov Substitution Principle (LSP)**
- All product subclasses can replace base Product class

### Technical Improvements
- **Pydantic Integration**: Type-safe data validation
- **Error Logging**: Structured logging system
- **Report Generation**: Automated low-stock reports
- **Clean Architecture**: Modular, testable code

### Data Validation Example
```python
# Automatic validation with Pydantic
product = FoodItem(
    product_id=101,
    product_name="Milk",
    price=45.0,
    quantity=20,
    expiry_date="2025-08-30"
)
```

---

##  Week 4: Test-Driven Development

**Branch**: `feat/week-4` → `develop`

### Goals Achieved
-  Implemented comprehensive test suite
-  Achieved almost 99% test coverage
-  Applied TDD methodology
-  Used advanced pytest features

### Test Structure
```
tests/
├── conftest.py                     # Shared fixtures
├── test_core.py                   # Core functionality tests
├── test_models.py                 # Model validation tests
├── test_models_using_fixtures.py  # Fixture-based tests
└── test_utils.py                  # Utility function tests
```

### TDD Approach: Red-Green-Refactor

1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

##  Overall Project Progression

### Technical Evolution

| Week | Paradigm | Key Concepts | Code Quality |
|------|----------|-------------|--------------|
| 1 | Scripting | Git, Python basics | Basic structure |
| 2 | Procedural | Data structures, file I/O | Error handling |
| 3 | Object-Oriented | Classes, inheritance, SOLID | Clean architecture |
| 4 | Test-Driven | Testing, mocking, coverage | Production-ready |

### Skills Demonstrated

**Version Control**
- Git workflow with feature branches
- Pull request process
- Code review integration

**Python Proficiency**
- Progression from basic to advanced concepts
- Clean, Pythonic code practices
- Industry-standard tools and libraries

**Software Design**
- SOLID principles application
- Clean architecture patterns
- Separation of concerns

**Quality Assurance**
- Test-driven development
- Comprehensive test coverage
- Continuous integration practices

### Industry Best Practices

- **Code Formatting**: Black, Ruff integration
- **Documentation**: Comprehensive README and docs
- **Error Handling**: Proper exception management
- **Logging**: Structured logging approach
- **Testing**: TDD with pytest
- **Architecture**: Modular, extensible design

---

### Week 5: API Development with FastAPI
**Branch**: `feature/week-5 → develop`

### Goals Achieved
- Implemented REST API using FastAPI
- Added routing for inventory endpoints
- Integrated API with InventoryManager
- Created automated API tests using pytest and TestClient
- Updated requirements.txt for new dependencies

## Project Structure
```
Week_5/
├── api/
│   ├── __init__.py
│   └── routes.py          # API routes for inventory operations
├── app.py                  # FastAPI application entry point
├── requirements.txt        # Includes FastAPI, Uvicorn
└── tests/
    └── test_routes.py      # API endpoint tests
```
## Key Features

- Routing: CRUD endpoints for inventory management
- Integration: API layer communicates with core business logic
- Testing: Endpoint validation with pytest and fastapi.testclien

**Example Endpoint**
```
@app.get("/inventory")
def get_inventory():
    return inventory_manager.get_all_products()

```

### Week 6 & 7: Database Integration, Flask API & Authentication
**Branch**: `feat/week-6 → develop`

### Goals Achieved
- Integrated Flask with SQLAlchemy ORM for database operations
- Implemented Alembic migrations for schema versioning
- Designed Pydantic schemas for request/response validation
- Added CRUD API endpoints for products
- Created database seeding scripts with CSV data
- Implemented User model with role-based access
- Added /auth/register endpoint with secure password hashing (Werkzeug)
- Integrated JWT-based authentication for session-less login
- Improved test coverage with database fixtures and API tests
- Updated config.py to load secrets & DB connection from .env
- Created .env.example for project setup

## Project Structure
```
Week_6_and_7/
├── api/
│   ├── app.py              # Flask app entry point
│   ├── config.py           # Config (PostgreSQL / SQLite support)
│   ├── db.py               # SQLAlchemy database instance
│   ├── __init__.py         # App factory
│   ├── models.py           # Product + User models
│   ├── routes.py           # CRUD API routes
│   ├── seed.py             # Database seeding logic
│   ├── schemas/            # Request & response schemas
│   │   ├── __init__.py
│   │   ├── request.py
│   │   └── response.py
│   └── security/           # Security & authentication
│       ├── __init__.py
│       ├── auth.py         # Authentication endpoints (/auth/register, login, etc.)
│       ├── jwt_utils.py    # JWT encode/decode helpers
│       └── password.py     # Password hashing & verification
├── data/
│   └── products.csv        # Sample seed data
├── instance/
│   └── inventory.db        # SQLite DB (optional)
├── migrations/             # Alembic migration files
│   
├── tests/                  # Unit & integration tests
│   ├── conftest.py         # Shared pytest fixtures
│   ├── test_auth.py        # Auth tests
│   ├── test_models.py      # Database model tests
│   ├── test_password.py    # Password tests
│   ├── test_routes_api.py  # API tests
│   └── test_seed.py        # Seeder tests
├── data/                   # (already included above, but double-check no duplicate)
│   └── products.csv
├── .env.example            # Example environment file
├── README.md               # Project setup & documentation
└── requirements.txt        # Python dependencies

```

## Key Features

Database Models:
Product, FoodItem, ElectronicItem, BookItem implemented via SQLAlchemy.

Migrations:
Alembic used for version-controlled schema updates.

Seeding:
seed.py reads from data/products.csv and populates DB.

API Endpoints:

GET /products → List all products
GET /products/<id> → Get single product
POST /products → Add new product
PUT /products/<id> → Update product
DELETE /products/<id> → Remove product

Validation:
Pydantic schemas for request & response models.

Testing:
Fixtures for DB setup/teardown
API route testing with pytest
Coverage improved to ~98%


### Week 8 – LLMs, Embeddings, and Retrieval-Augmented Generation (RAG)

**Overview**

This week marks the transition from traditional software engineering to the AI stack.
The goal was to understand Large Language Models (LLMs), embeddings, and the Retrieval-Augmented Generation (RAG) pattern — and finally, to build an Inventory Chatbot API that allows natural language queries on product data stored in a PostgreSQL database with pgvector.

## Project Structure
```
Week_8/
├── api/                      # Flask application
│   ├── app.py                # App entrypoint
│   ├── chat_routes.py        # Chat (RAG) blueprint and endpoint
│   ├── config.py             # App config (loads .env values)
│   ├── db.py                 # SQLAlchemy setup
│   ├── __init__.py           # App factory, blueprint registration
│   ├── models.py             # SQLAlchemy models
│   ├── routes.py             # Product routes (CRUD)
│   ├── schemas/              # Pydantic request/response validation
│   ├── security/             # Auth (JWT, password hashing, decorators)
│   └── seed.py               # DB seeding
├── data/
│   └── products.csv          # Sample product data
├── migrations/               # Alembic migration files
├── requirements.txt          # Python dependencies
└── scripts/                  # Utility scripts for RAG and embeddings
    ├── constants.py          # Constants (models, chunk sizes, etc.)
    ├── data_loader.py        # Load products from DB
    ├── rag_chain.py          # RAG pipeline (retriever → prompt → LLM)
    ├── embedding.py          # Embedding generation
    ├── storage.py            # PGVector integration
    └── query_gpt.py          # Direct LLM query helper

```

##  Next Steps & Potential Enhancements

### Advanced Features
- [ ] Docker containerization
- [ ] CI/CD pipeline setup
- [ ] Performance monitoring
- [ ] Microservices architecture

### Learning Outcomes

This journey demonstrates:
- **Progressive Learning**: Building complexity week by week
- **Best Practices**: Following industry standards throughout
- **Problem Solving**: Addressing real-world software challenges
- **Quality Focus**: Emphasis on testing and maintainability

---

*This development journey showcases a methodical approach to learning Python and software engineering principles, resulting in a production-ready application.*
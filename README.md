# Inventory Manager

A comprehensive **Python-based Inventory Management System** built using Object-Oriented Programming principles, following Test-Driven Development practices. This project demonstrates a complete software development lifecycle from basic Python scripting to a production-ready application.

##  Quick Start

```bash
# Clone the repository
git clone <your-repo-url>
cd inventory-manager

# Set up virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

##  Features

- **Multi-product type support**: Food items, Electronics, Books with specific attributes
- **Data validation**: Using Pydantic v2 for robust data handling
- **Automated reporting**: Low stock alerts and error logging
- **CLI interface**: Easy-to-use command-line interaction
- **Comprehensive testing**: 99% test coverage with pytest
- **Clean architecture**: Following SOLID principles


##  Project Structure

```
inventory-manager/
├── Week_1/                     # Git workflow and Python basics
├── Week_2/                     # Data structures and file handling
├── Week_3/                     # OOP implementation
├── Week_4/                     # Comprehensive test suite
├── Week_5/                     # API implementation
├── Week_6_and7/                # Comprehensive test suite and user authentication
├── Week_8/                     # LLMs, Embeddings, and Retrieval-Augmented Generation (RAG)
├── docs/                       # Detailed documentation
├── .gitignore                  # Git ignore rules for virtual environments, __pycache__, etc.
├── .pre-commit-config.yaml     # Pre-commit hooks configuration for code quality checks
├── pyproject.toml              # Project configuration (tool settings, linters, formatters)
├── pytest.ini                  # Pytest configuration for test discovery and reporting
├── README.md                   # High-level project overview and instructions
├── setup.md                    # Local setup guide and development environment instructions
```

##  Testing

This project follows **Test-Driven Development (TDD)** practices:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=inventory_manager

# Run specific test file
pytest tests/test_core.py -v
```

**Current test coverage: 100%**

##  Documentation

Comprehensive documentation is available in the `docs/` folder:

- **[Setup Guide](docs/SETUP.md)** - Detailed installation and configuration
- **[Development Journey](docs/DEVELOPMENT.md)** - Week-by-week learning progress
- **[Architecture Guide](docs/ARCHITECTURE.md)** - Technical design and patterns
- **[Testing Strategy](docs/TESTING.md)** - TDD approach and test coverage

##  Technology Stack

- **Python 3.10+**
- **Pydantic v2** - Data validation and serialization
- **Pytest** - Testing framework
- **Black & Ruff** - Code formatting and linting
- **CSV** - Data storage and processing

##  Learning Outcomes

This project demonstrates proficiency in:

- **Git workflow** and version control best practices
- **Python fundamentals** and advanced concepts
- **Object-Oriented Programming** principles
- **Test-Driven Development** methodology
- **Code quality** tools and practices
- **Documentation** and project organization

##  Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


##  Contact

**Vansh Jaiswal** - vanshjaiswal@bitcot.com

Project Link: [https://github.com/Vanshbit138/inventory-manager.git](https://github.com/Vanshbit138/inventory-manager.git)

---

*Built as part of a comprehensive Python learning journey*
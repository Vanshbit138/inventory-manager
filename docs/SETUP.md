# Setup Guide

This guide provides detailed instructions for setting up the Inventory Manager project on your local machine.

## 📋 Prerequisites

- **Python 3.10 or higher** - [Download Python](https://python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** (comes with Python)

### Verify Prerequisites

```bash
python --version    # Should show 3.10+
git --version      # Should show git version
pip --version      # Should show pip version
```

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd inventory-manager
```

### 2. Create Virtual Environment

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Run tests to ensure everything works
pytest

# Run the main application
python main.py
```

## 📁 Project Structure Overview

```
inventory-manager/
├── data/
│   └── products.csv              # Sample product data
├── docs/                        # Documentation files
├── inventory_manager/           # Main application package
│   ├── __init__.py
│   ├── core.py                 # Business logic
│   ├── models.py               # Data models
│   └── utils.py                # Utilities
├── tests/                      # Test suite
├── Week-1/                     # Learning progression
├── Week-2/                     # (weeks show development journey)
├── Week-3/
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
└── README.md                   # Project overview
```

## 🔧 Configuration

### Sample Data Setup

The application uses `data/products.csv` for sample data. The CSV format should be:

```csv
product_id,product_name,type,price,quantity,expiry_date,warranty_period,author,pages
101,Milk,food,45.0,20,2025-08-30,,,
102,Laptop,electronic,60000.0,5,,12,,
103,Python 101,book,399.0,15,,,John Doe,320
```


## 🧪 Development Setup

### Code Quality Tools

The project uses several code quality tools:

```bash
# Format code
black .

# Lint code
ruff check .


### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=inventory_manager

# Run specific test file
pytest tests/test_core.py

# Run specific test function
pytest tests/test_core.py::test_get_inventory_value
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'inventory_manager'`
**Solution**: Ensure you're in the project root directory and virtual environment is activated.

**Issue**: `FileNotFoundError: data/products.csv`
**Solution**: Create the `data/products.csv` file with sample data or run from the correct directory.

**Issue**: Virtual environment not activating
**Solution**: 
- On Windows: Use `venv\Scripts\activate.bat` instead of `activate`
- Ensure you created the venv in the correct directory

### Getting Help

If you encounter issues:

1. Check that all prerequisites are installed correctly
2. Ensure virtual environment is activated
3. Verify you're in the correct directory
4. Check the error logs in `error.log`
5. Run tests to identify specific issues: `pytest -v`

## 🔄 Updates

To update the project dependencies:

```bash
pip install -r requirements.txt --upgrade
```

To update the project code:

```bash
git pull origin main
```

## 📚 Next Steps

After successful setup:

1. Read the [Development Journey](development-journey.md) to understand the project evolution
2. Check the [Architecture Guide](architecture.md) for technical details  
3. Explore the [Testing Strategy](testing.md) to understand the test approach
4. Review [API Reference](api-reference.md) for code documentation

---

*Need help? Check the main [README.md](../README.md) or open an issue in the repository.*
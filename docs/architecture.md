# Architecture Guide

This document provides a detailed technical overview of the Inventory Manager's architecture, design patterns, and implementation decisions.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Layer    │    │  Business Logic  │    │  Presentation   │
│                 │    │                  │    │                 │
│ • CSV Files     │◄──►│ • InventoryManager│◄──►│ • CLI Interface │
│ • Error Logs    │    │ • Product Models │    │ • Reports       │
│ • Reports       │    │ • Validation     │    │ • Logging       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Package Structure

```
inventory_manager/
├── __init__.py          # Package initialization
├── core.py             # Core business logic
├── models.py           # Data models and validation
└── utils.py            # Utility functions
```

## 🎯 Design Principles

### SOLID Principles Implementation

#### Single Responsibility Principle (SRP)
Each class and module has a single, well-defined responsibility:

- **`core.py`**: Inventory management operations only
- **`models.py`**: Data representation and validation only  
- **`utils.py`**: Helper functions and utilities only

#### Open/Closed Principle (OCP)
The system is designed to be open for extension but closed for modification:

```python
# Easy to add new product types without modifying existing code
class Product(BaseModel):  # Base class remains unchanged
    # Common attributes

class NewProductType(Product):  # Extension via inheritance
    # Type-specific attributes
```

#### Liskov Substitution Principle (LSP)
All product subclasses can be used interchangeably:

```python
def process_product(product: Product):  # Works with any Product subclass
    return product.calculate_value()
```

#### Interface Segregation Principle (ISP)
Interfaces are focused and specific to client needs.

#### Dependency Inversion Principle (DIP)
High-level modules don't depend on low-level implementation details.

## 📊 Data Models

### Class Hierarchy

```python
Product (BaseModel)
├── FoodItem
│   ├── expiry_date: Optional[str]
│   └── is_expired() -> bool
├── ElectronicItem  
│   ├── warranty_period: Optional[int]
│   └── has_warranty() -> bool
└── BookItem
    ├── author: Optional[str]
    ├── pages: Optional[int]
    └── calculate_reading_time() -> float
```

### Pydantic Integration

```python
from pydantic import BaseModel, validator
from typing import Optional

class Product(BaseModel):
    product_id: int
    product_name: str
    type: str
    price: float
    quantity: int
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
```

**Benefits:**
- **Type Safety**: Automatic type checking and conversion
- **Data Validation**: Built-in validation rules
- **Serialization**: Easy JSON/dict conversion
- **Documentation**: Self-documenting models

## 🔧 Core Components

### InventoryManager Class

**Responsibilities:**
- Load and parse inventory data
- Validate product information
- Generate reports and logs
- Manage product operations

**Key Methods:**

```python
class InventoryManager:
    def __init__(self, csv_file: str, low_stock_threshold: int = 10)
    
    def load_inventory(self) -> List[Product]
    def validate_products(self, products: List[dict]) -> List[Product]
    def generate_low_stock_report(self, products: List[Product]) -> None
    def run(self) -> None
```

### Product Factory Pattern

The system uses a factory pattern for creating product instances:

```python
def create_product(product_data: dict) -> Product:
    """Factory method to create appropriate product type"""
    product_type = product_data.get('type', '').lower()
    
    if product_type == 'food':
        return FoodItem(**product_data)
    elif product_type == 'electronic':
        return ElectronicItem(**product_data)
    elif product_type == 'book':
        return BookItem(**product_data)
    else:
        return Product(**product_data)
```

## 📁 File Structure & Responsibilities

### core.py
```python
class InventoryManager:
    """Main business logic coordinator"""
    - Data loading and processing
    - Orchestration of operations
    - Error handling and logging
```

### models.py
```python
# Data representation layer
class Product(BaseModel):           # Base product model
class FoodItem(Product):           # Food-specific attributes
class ElectronicItem(Product):     # Electronics-specific attributes  
class BookItem(Product):           # Book-specific attributes
```

### utils.py
```python
# Utility functions
def setup_logging() -> logging.Logger
def write_report(filename: str, content: str) -> None
def calculate_total_value(products: List[Product]) -> float
```

## 🔄 Data Flow

### Typical Operation Flow

1. **Data Loading**
   ```
   CSV File → Raw Dict Data → Validation → Product Objects
   ```

2. **Processing**
   ```
   Product Objects → Business Logic → Calculations/Reports
   ```

3. **Output Generation**
   ```
   Results → File Writing → Log Generation → User Feedback
   ```

### Error Handling Flow

```
Error Occurs → Logging → Graceful Degradation → User Notification
```

## 🧪 Testing Architecture

### Test Organization

```
tests/
├── conftest.py                     # Shared test fixtures
├── test_core.py                   # Core business logic tests
├── test_models.py                 # Data model tests
└── test_utils.py                  # Utility function tests
```

### Testing Patterns

**Fixture-Based Testing**
```python
@pytest.fixture
def sample_products():
    return [
        {"product_id": 1, "product_name": "Milk", "type": "food"},
        {"product_id": 2, "product_name": "Laptop", "type": "electronic"}
    ]
```

**Parametrized Testing**
```python
@pytest.mark.parametrize("quantity,expected", [
    (5, True),    # Low stock
    (15, False),  # Normal stock
])
def test_is_low_stock(quantity, expected):
    assert is_low_stock(quantity) == expected
```

**Mock-Based Testing**
```python
@patch('inventory_manager.core.csv.DictReader')
def test_load_inventory_file_error(mock_reader):
    mock_reader.side_effect = FileNotFoundError()
    # Test error handling
```

## 📈 Performance Considerations

### Memory Management
- **Lazy Loading**: Data loaded on-demand
- **Generator Usage**: For large datasets
- **Memory-Efficient Data Structures**: Appropriate container types

### Scalability
- **Modular Design**: Easy to extend and modify
- **Loose Coupling**: Components can be replaced independently
- **Configuration-Driven**: Behavior controlled via settings

## 🔐 Error Handling Strategy

### Error Categories

1. **Data Validation Errors**: Invalid CSV data, type mismatches
2. **File I/O Errors**: Missing files, permission issues
3. **Business Logic Errors**: Invalid operations, constraint violations

### Error Handling Approach

```python
try:
    # Operation
    result = risky_operation()
except SpecificError as e:
    # Log the error
    logger.error(f"Specific error occurred: {e}")
    # Handle gracefully
    return default_value
except Exception as e:
    # Log unexpected errors
    logger.exception("Unexpected error occurred")
    # Re-raise or handle appropriately
    raise
```

## 🚀 Extension Points

### Adding New Product Types

1. **Create New Model Class**
   ```python
   class NewProductType(Product):
       special_attribute: Optional[str] = None
       
       def special_method(self) -> str:
           return f"Special: {self.special_attribute}"
   ```

2. **Update Factory Method**
   ```python
   def create_product(product_data: dict) -> Product:
       # Add new case
       elif product_type == 'newtype':
           return NewProductType(**product_data)
   ```

3. **Add Tests**
   ```python
   def test_new_product_type():
       product = NewProductType(special_attribute="value")
       assert product.special_method() == "Special: value"
   ```

### Adding New Features

The architecture supports easy feature addition:

- **New Reports**: Add methods to `utils.py`
- **New Validations**: Add validators to models
- **New Operations**: Extend `InventoryManager` class

## 📊 Dependencies

### Core Dependencies
- **pydantic**: Data validation and serialization
- **typing**: Type hints and annotations
- **csv**: Data file processing
- **logging**: Error and operation logging

### Development Dependencies  
- **pytest**: Testing framework
- **black**: Code formatting
- **ruff**: Linting and code quality
- **coverage**: Test coverage analysis

## 🔄 Future Architecture Considerations

### Potential Enhancements

1. **Database Integration**
   ```
   CSV Files → SQLite/PostgreSQL → ORM Layer
   ```

2. **API Layer**
   ```
   CLI → REST API → Service Layer → Data Layer
   ```

3. **Microservices**
   ```
   Monolith → Product Service + Inventory Service + Report Service
   ```

4. **Event-Driven Architecture**
   ```
   Direct Calls → Event Bus → Event Handlers
   ```

---

*This architecture provides a solid foundation for a maintainable, extensible, and testable inventory management system.*
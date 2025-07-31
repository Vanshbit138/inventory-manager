import csv
import logging
from typing import List
from pydantic import BaseModel, ValidationError, field_validator

# Set up logging
logging.basicConfig(filename='errors.log', level=logging.ERROR, filemode='w')

# Threshold for low stock report
LOW_STOCK_THRESHOLD = 10

# Define Product model using Pydantic v2
class Product(BaseModel):
    """
    Represents a product with validation rules using Pydantic.
    
    Attributes:
        product_id (int): Unique identifier for the product.
        product_name (str): Name of the product.
        quantity (int): Available quantity of the product (must be non-negative).
        price (float): Price of the product (must be positive).
    """

    product_id: int
    product_name: str
    quantity: int
    price: float

    @field_validator('quantity')
    @classmethod
    def check_quantity(cls, v):
        """
        Validates that the quantity is non-negative.
        
        Args:
            v (int): The quantity value.
        
        Returns:
            int: Validated quantity value.
        
        Raises:
            ValueError: If quantity is negative.
        """
        if v < 0:
            raise ValueError("Quantity must be non-negative")
        return v

    @field_validator('price')
    @classmethod
    def check_price(cls, v):
        """
        Validates that the price is a positive number.
        
        Args:
            v (float): The price value.
        
        Returns:
            float: Validated price value.
        
        Raises:
            ValueError: If price is not positive.
        """
        if v <= 0:
            raise ValueError("Price must be a positive number")
        return v

def load_and_validate_products(csv_file: str) -> List[Product]:
    """
    Loads product data from a CSV file and validates each row using the Product model.
    Invalid rows are logged to 'errors.log'.
    
    Args:
        csv_file (str): Path to the CSV file containing product data.
    
    Returns:
        List[Product]: A list of valid Product instances.
    """
    valid_products = []

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for line_number, row in enumerate(reader, start=2):  # Start at 2 to skip header
            try:
                product = Product(**row)
                valid_products.append(product)
            except ValidationError as e:
                for err in e.errors():
                    error_msg = f"Line {line_number}: {row} - {err['loc'][0]}: {err['msg']}"
                    logging.error(error_msg)

    return valid_products

def generate_low_stock_report(products: List[Product], threshold: int, report_file: str):
    """
    Generates a low stock report for products below the specified threshold.
    
    Args:
        products (List[Product]): List of validated products.
        threshold (int): Quantity threshold for low stock.
        report_file (str): Output file path for the report.
    """
    with open(report_file, 'w') as file:
        file.write("Low Stock Products (Quantity < {}):\n\n".format(threshold))
        for product in products:
            if product.quantity < threshold:
                file.write(f"{product.product_name} - Quantity: {product.quantity}\n")

def main():
    """
    Main function to load, validate, and process inventory data.
    It generates a low stock report after validation.
    """
    products = load_and_validate_products('inventory.csv')
    generate_low_stock_report(products, LOW_STOCK_THRESHOLD, 'low_stock_report.txt')

if __name__ == "__main__":
    main()

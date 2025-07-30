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
    product_id: int
    product_name: str
    quantity: int
    price: float

    @field_validator('quantity')
    @classmethod
    def check_quantity(cls, v):
        if v < 0:
            raise ValueError("Quantity must be non-negative")
        return v

    @field_validator('price')
    @classmethod
    def check_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be a positive number")
        return v

# Function to load and validate CSV rows
def load_and_validate_products(csv_file: str) -> List[Product]:
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

# Function to generate a low stock report
def generate_low_stock_report(products: List[Product], threshold: int, report_file: str):
    with open(report_file, 'w') as file:
        file.write("Low Stock Products (Quantity < {}):\n\n".format(threshold))
        for product in products:
            if product.quantity < threshold:
                file.write(f"{product.product_name} - Quantity: {product.quantity}\n")

# Main entry point
def main():
    products = load_and_validate_products('inventory.csv')
    generate_low_stock_report(products, LOW_STOCK_THRESHOLD, 'low_stock_report.txt')

if __name__ == "__main__":
    main()

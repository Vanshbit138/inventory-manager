import csv
from pydantic import BaseModel, ValidationError, field_validator
from typing import List

# Step 1: Define the InventoryItem model using Pydantic v2 style
class InventoryItem(BaseModel):
    item_name: str
    quantity: int
    price: float

    @field_validator('quantity')
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError('Quantity must be non-negative')
        return v

    @field_validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be non-negative')
        return v

# Step 2: Read and validate inventory from CSV
valid_items = []
invalid_items = []

with open('inventory.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for line_number, row in enumerate(reader, start=2):  # start=2 to match line number in CSV (header is line 1)
        try:
            item = InventoryItem(**row)
            valid_items.append(item)
        except ValidationError as e:
            invalid_items.append((line_number, row, e.errors()))

# Step 3: Print Valid Items
print("\n VALID ITEMS:")
for item in valid_items:
    print(item.model_dump())  # instead of deprecated .dict()

# Step 4: Print Invalid Items
print("\n INVALID ITEMS:\n")
for line, row, errors in invalid_items:
    print(f"Line {line}: {row}")
    for err in errors:
        print(f" - {err['loc'][0]}: {err['msg']}")

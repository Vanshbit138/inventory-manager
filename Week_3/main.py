from inventory_manager.core import Inventory


def main():
    inventory = Inventory()
    inventory.load_from_csv("data/products.csv")
    inventory.generate_report()


if __name__ == "__main__":
    main()

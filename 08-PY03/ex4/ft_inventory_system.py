#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Inventory System Analysis ===")
    raw_args = sys.argv[1:]
    inventory: dict[str, int] = {}

    for arg in raw_args:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue
        parts = arg.split(":", 1)
        item = parts[0]
        val_str = parts[1]

        if item in inventory:
            print(f"Redundant item '{item}' - discarding")
            continue

        try:
            qty = int(val_str)
            inventory[item] = qty
        except ValueError as e:
            print(f"Quantity error for '{item}': {e}")

    print(f"Got inventory: {inventory}")
    items_list = list(inventory.keys())
    print(f"Item list: {items_list}")

    total_qty = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total_qty}")

    for item, qty in inventory.items():
        pct = round((qty / total_qty) * 100, 1) if total_qty > 0 else 0.0
        print(f"Item {item} represents {pct}%")

    if inventory:
        most_item = ""
        most_qty = -1
        least_item = ""
        least_qty = -1

        for item, qty in inventory.items():
            if most_qty == -1 or qty > most_qty:
                most_item = item
                most_qty = qty
            if least_qty == -1 or qty < least_qty:
                least_item = item
                least_qty = qty

        print(
            f"Item most abundant: {most_item} "
            f"with quantity {most_qty}"
        )
        print(
            f"Item least abundant: {least_item} "
            f"with quantity {least_qty}"
        )

    updated_inv = dict(inventory)
    updated_inv.update({"magic_item": 1})
    print(f"Updated inventory: {updated_inv}")


if __name__ == "__main__":
    main()

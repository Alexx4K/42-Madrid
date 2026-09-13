def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:

    seed_type = seed_type.capitalize()
    unit_types = ["grams", "packets", "area"]
    if unit not in unit_types:
        print("Unknown unit type")
    elif unit == "grams":
        print(f"{seed_type} seeds: {quantity} {unit} total")
    elif unit == "packets":
        print(f"{seed_type} seeds: {quantity} {unit} available")
    elif unit == "area":
        print(f"{seed_type} seeds: covers {quantity} square meters")

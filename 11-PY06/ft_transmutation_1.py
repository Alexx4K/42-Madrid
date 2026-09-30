import alchemy.transmutation


def main() -> None:
    print("=== Transmutation 1 ===")
    print("Import transmutation module directly")
    result = alchemy.transmutation.lead_to_gold()
    print(f"Testing lead to gold: {result}")


if __name__ == "__main__":
    main()

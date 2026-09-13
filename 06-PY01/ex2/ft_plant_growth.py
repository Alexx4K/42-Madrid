#!/usr/bin/env python3


class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: float = 0.0
        self.age: int = 0

    def grow(self, amount: float = 0.8) -> None:
        self.height = round(self.height + amount, 1)

    def add_age(self, days: int = 1) -> None:
        self.age += days

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main() -> None:
    p = Plant()
    p.name = "Rose"
    p.height = 25.0
    p.age = 30

    print("=== Garden Plant Growth ===")
    p.show()
    initial_height = p.height

    for day in range(1, 8):
        p.grow(0.8)
        p.add_age(1)
        print(f"=== Day {day} ===")
        p.show()

    total_growth = round(p.height - initial_height, 1)
    print(f"Growth this week: {total_growth}cm")


if __name__ == "__main__":
    main()

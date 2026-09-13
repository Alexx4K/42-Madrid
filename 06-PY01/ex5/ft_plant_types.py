#!/usr/bin/env python3


class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = float(height)
        self._age: int = age

    def grow(self, amount: float = 1.0) -> None:
        self._height = round(self._height + amount, 1)

    def age(self, days: int = 1) -> None:
        self._age += days

    def show(self) -> None:
        print(f"{self._name}: {self._height}cm, {self._age} days old")


class Flower(Plant):
    def __init__(
        self, name: str, height: float, age: int, color: str
    ) -> None:
        super().__init__(name, height, age)
        self.color: str = color
        self.is_blooming: bool = False

    def bloom(self) -> None:
        self.is_blooming = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self.color}")
        if self.is_blooming:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(
        self, name: str, height: float, age: int, trunk_diameter: float
    ) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter: float = float(trunk_diameter)

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self._height}cm long and {self.trunk_diameter}cm wide."
        )

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter}cm")


class Vegetable(Plant):
    def __init__(
        self, name: str, height: float, age: int, harvest_season: str
    ) -> None:
        super().__init__(name, height, age)
        self.harvest_season: str = harvest_season
        self.nutritional_value: int = 0

    def grow(self, amount: float = 1.0) -> None:
        super().grow(amount)
        self.nutritional_value += 1

    def age(self, days: int = 1) -> None:
        super().age(days)
        self.nutritional_value += days

    def show(self) -> None:
        super().show()
        print(f"Harvest season: {self.harvest_season}")
        print(f"Nutritional value: {self.nutritional_value}")


def main() -> None:
    print("=== Garden Plant Types ===")
    print("=== Flower")
    f = Flower("Rose", 15.0, 10, "red")
    f.show()
    print("[asking the rose to bloom]")
    f.bloom()
    f.show()

    print("=== Tree")
    t = Tree("Oak", 200.0, 365, 5.0)
    t.show()
    print("[asking the oak to produce shade]")
    t.produce_shade()

    print("=== Vegetable")
    v = Vegetable("Tomato", 5.0, 10, "April")
    v.show()
    print("[make tomato grow and age for 20 days]")
    v.grow(42.0)
    v.age(20)
    v.show()


if __name__ == "__main__":
    main()

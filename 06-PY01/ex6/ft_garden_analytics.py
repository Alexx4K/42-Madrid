#!/usr/bin/env python3


class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls: int = 0
            self._age_calls: int = 0
            self._show_calls: int = 0

        def increment_grow(self) -> None:
            self._grow_calls += 1

        def increment_age(self) -> None:
            self._age_calls += 1

        def increment_show(self) -> None:
            self._show_calls += 1

        def display(self) -> None:
            print(
                f"Stats: {self._grow_calls} grow, "
                f"{self._age_calls} age, "
                f"{self._show_calls} show"
            )

    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = float(height)
        self._age: int = age
        self.stats: Plant.Stats = self.Stats()

    def grow(self, amount: float = 1.0) -> None:
        self._height = round(self._height + amount, 1)
        self.stats.increment_grow()

    def age(self, days: int = 1) -> None:
        self._age += days
        self.stats.increment_age()

    def show(self) -> None:
        self.stats.increment_show()
        print(f"{self._name}: {self._height}cm, {self._age} days old")

    @staticmethod
    def is_older_than_year(days: int) -> bool:
        return days > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    def display_stats(self) -> None:
        self.stats.display()


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
        self._shade_calls: int = 0

    def produce_shade(self) -> None:
        self._shade_calls += 1
        print(
            f"Tree {self._name} now produces a shade of "
            f"{self._height}cm long and {self.trunk_diameter}cm wide."
        )

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {self.trunk_diameter}cm")

    def display_shade_stats(self) -> None:
        print(f"{self._shade_calls} shade")

    def display_stats(self) -> None:
        super().display_stats()
        self.display_shade_stats()


class Seed(Flower):
    def __init__(
        self, name: str, height: float, age: int, color: str
    ) -> None:
        super().__init__(name, height, age, color)
        self.seeds_count: int = 0

    def bloom(self) -> None:
        super().bloom()
        self.seeds_count = 42

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self.seeds_count}")


def main() -> None:
    print("=== Garden statistics ===")
    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(
        f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}"
    )
    print("=== Flower")
    f = Flower("Rose", 15.0, 10, "red")
    f.show()
    print("[statistics for Rose]")
    f.display_stats()
    print("[asking the rose to grow and bloom]")
    f.grow(8.0)
    f.bloom()
    f.show()
    print("[statistics for Rose]")
    f.display_stats()
    print("=== Tree")
    t = Tree("Oak", 200.0, 365, 5.0)
    t.show()
    print("[statistics for Oak]")
    t.display_stats()
    print("[asking the oak to produce shade]")
    t.produce_shade()
    print("[statistics for Oak]")
    t.display_stats()
    print("=== Seed")
    s = Seed("Sunflower", 80.0, 45, "yellow")
    s.show()
    print("[make sunflower grow, age and bloom]")
    s.grow(30.0)
    s.age(20)
    s.bloom()
    s.show()
    print("[statistics for Sunflower]")
    s.display_stats()
    print("=== Anonymous")
    anon = Plant.create_anonymous()
    anon.show()
    print("[statistics for Unknown plant]")
    anon.display_stats()


if __name__ == "__main__":
    main()

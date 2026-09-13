#!/usr/bin/env python3


class Plant:
    def __init__(self) -> None:
        self.name: str = ""
        self.height: int = 0
        self.age: int = 0

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age} days old")


def main() -> None:
    p1 = Plant()
    p1.name = "Rose"
    p1.height = 25
    p1.age = 30

    p2 = Plant()
    p2.name = "Sunflower"
    p2.height = 80
    p2.age = 45

    p3 = Plant()
    p3.name = "Cactus"
    p3.height = 15
    p3.age = 120

    print("=== Garden Plant Registry ===")
    p1.show()
    p2.show()
    p3.show()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3


class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self._name: str = name
        self._height: float = 0.0
        self._age: int = 0
        self.set_height(height)
        self.set_age(age)

    def get_height(self) -> float:
        return self._height

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = float(height)

    def get_age(self) -> int:
        return self._age

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = age

    def show(self) -> None:
        print(f"{self._name}: {self._height}cm, {self._age} days old")


def main() -> None:
    print("=== Garden Security System ===")
    p = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    p.show()

    p.set_height(25.0)
    print("Height updated: 25cm")

    p.set_age(30)
    print("Age updated: 30 days")

    p.set_height(-5.0)
    p.set_age(-10)

    print("Current state: ", end="")
    p.show()


if __name__ == "__main__":
    main()

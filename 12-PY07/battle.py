#!/usr/bin/env python3

from ex0 import AquaFactory, CreatureFactory, FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(f1: CreatureFactory, f2: CreatureFactory) -> None:
    print("Testing battle")
    c1 = f1.create_base()
    c2 = f2.create_base()
    print(c1.describe())
    print("VS.")
    print(c2.describe())
    print("fight!")
    print(c1.attack())
    print(c2.attack())


def main() -> None:
    flame_fact = FlameFactory()
    aqua_fact = AquaFactory()
    test_factory(flame_fact)
    test_factory(aqua_fact)
    test_battle(flame_fact, aqua_fact)


if __name__ == "__main__":
    main()

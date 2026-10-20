#!/usr/bin/env python3

from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


def test_healing() -> None:
    print("Testing Creature with healing capability")
    factory = HealingCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, HealCapability):
        print(base.heal())

    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, HealCapability):
        print(evolved.heal())


def test_transform() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, TransformCapability):
        print(base.transform())
        print(base.attack())
        print(base.revert())

    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, TransformCapability):
        print(evolved.transform())
        print(evolved.attack())
        print(evolved.revert())


def main() -> None:
    test_healing()
    test_transform()


if __name__ == "__main__":
    main()

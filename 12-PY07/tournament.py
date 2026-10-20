#!/usr/bin/env python3

from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def run_tournament(
    title: str,
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    print(f"*** {title} ***")
    print(f"{len(opponents)} opponents involved")

    teams = []
    for fact, strat in opponents:
        creature = fact.create_base()
        teams.append((creature, strat))

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            c1, s1 = teams[i]
            c2, s2 = teams[j]
            print("* Battle *")
            print(c1.describe())
            print("VS.")
            print(c2.describe())
            print("now fight!")
            try:
                s1.act(c1)
                s2.act(c2)
            except InvalidStrategyError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


def main() -> None:
    t0 = [
        (FlameFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    run_tournament("Tournament", t0)

    t1 = [
        (FlameFactory(), AggressiveStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
    ]
    run_tournament("Tournament 1 (error)", t1)

    t2 = [
        (AquaFactory(), NormalStrategy()),
        (HealingCreatureFactory(), DefensiveStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
    ]
    run_tournament("Tournament 2 (multiple)", t2)


if __name__ == "__main__":
    main()

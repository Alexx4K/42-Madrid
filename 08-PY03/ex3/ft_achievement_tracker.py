#!/usr/bin/env python3

import random


ACHIEVEMENTS = [
    "Crafting Genius",
    "World Savior",
    "Master Explorer",
    "Collector Supreme",
    "Untouchable",
    "Boss Slayer",
    "Strategist",
    "Unstoppable",
    "Speed Runner",
    "Survivor",
    "Treasure Hunter",
    "First Steps",
    "Sharp Mind",
    "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    count = random.randint(5, 9)
    return set(random.sample(ACHIEVEMENTS, count))


def main() -> None:
    print("=== Achievement Tracker System ===")
    players = {
        "Alice": gen_player_achievements(),
        "Bob": gen_player_achievements(),
        "Charlie": gen_player_achievements(),
        "Dylan": gen_player_achievements(),
    }

    for name, achs in players.items():
        print(f"Player {name}: {achs}")

    all_achievements: set[str] = set()
    for achs in players.values():
        all_achievements = all_achievements.union(achs)
    print(f"All distinct achievements: {all_achievements}")

    common_achievements = set(ACHIEVEMENTS)
    for achs in players.values():
        common_achievements = common_achievements.intersection(achs)
    print(f"Common achievements: {common_achievements}")

    for name, achs in players.items():
        other_achs: set[str] = set()
        for other_name, other_set in players.items():
            if name != other_name:
                other_achs = other_achs.union(other_set)
        only_player = achs.difference(other_achs)
        print(f"Only {name} has: {only_player}")

    for name, achs in players.items():
        missing = set(ACHIEVEMENTS).difference(achs)
        print(f"{name} is missing: {missing}")


if __name__ == "__main__":
    main()

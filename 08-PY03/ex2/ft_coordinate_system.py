#!/usr/bin/env python3

import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        raw = input("Enter new coordinates as floats in format 'x,y,z': ")
        parts = raw.split(",")
        if len(parts) != 3:
            print("Invalid syntax")
            continue
        try:
            coords: list[float] = []
            for p in parts:
                clean_p = p.strip()
                try:
                    coords.append(float(clean_p))
                except ValueError:
                    print(
                        f"Error on parameter '{clean_p}': "
                        f"could not convert string to float: '{clean_p}'"
                    )
                    raise ValueError
            return (coords[0], coords[1], coords[2])
        except ValueError:
            pass


def main() -> None:
    print("=== Game Coordinate System ===")
    print("Get a first set of coordinates")
    p1 = get_player_pos()
    print(f"Got a first tuple: {p1}")
    print(f"It includes: X={p1[0]}, Y={p1[1]}, Z={p1[2]}")
    dist_center = round(
        math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2), 4
    )
    print(f"Distance to center: {dist_center}")

    print("Get a second set of coordinates")
    p2 = get_player_pos()
    dist_p1_p2 = round(
        math.sqrt(
            (p2[0] - p1[0]) ** 2
            + (p2[1] - p1[1]) ** 2
            + (p2[2] - p1[2]) ** 2
        ),
        4,
    )
    print(f"Distance between the 2 sets of coordinates: {dist_p1_p2}")


if __name__ == "__main__":
    main()

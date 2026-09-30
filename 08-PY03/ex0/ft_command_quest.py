#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== Command Quest ===")
    print(f"Program name: {sys.argv[0]}")
    args = sys.argv[1:]
    if not args:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(args)}")
        for i, arg in enumerate(args, start=1):
            print(f"Argument {i}: {arg}")
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()

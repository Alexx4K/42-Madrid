#!/usr/bin/env python3

import sys


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return

    filepath = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filepath}'")

    try:
        f = open(filepath, "r")
        try:
            content = f.read()
            print(content, end="")
        finally:
            f.close()
            print(f"File '{filepath}' closed.")
    except OSError as e:
        print(f"Error opening file '{filepath}': {e}")


if __name__ == "__main__":
    main()

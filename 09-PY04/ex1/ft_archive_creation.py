#!/usr/bin/env python3

import sys


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file>")
        return

    filepath = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filepath}'")

    content = ""
    try:
        f = open(filepath, "r")
        try:
            content = f.read()
            print(content, end="")
        finally:
            f.close()
            print(f"File '{filepath}' closed.")
    except Exception as e:
        print(f"Error opening file '{filepath}': {e}")
        return

    print("\nTransform data:")
    lines = content.splitlines()
    transformed_lines = [f"{line}#" for line in lines]
    transformed_content = "\n".join(transformed_lines)
    if transformed_lines:
        transformed_content += "\n"

    print(transformed_content, end="")

    out_name = input("Enter new file name (or empty): ").strip()
    if not out_name:
        print("Not saving data.")
        return

    print(f"Saving data to '{out_name}'")
    try:
        out_file = open(out_name, "w")
        try:
            out_file.write(transformed_content)
            print(f"Data saved in file '{out_name}'.")
        finally:
            out_file.close()
    except Exception as e:
        print(f"Error opening file '{out_name}': {e}")


if __name__ == "__main__":
    main()

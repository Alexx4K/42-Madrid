#!/usr/bin/env python3

import sys


def main() -> None:
    if len(sys.argv) != 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <file>\n")
        return

    filepath = sys.argv[1]
    sys.stdout.write("=== Cyber Archives Recovery & Preservation ===\n")
    sys.stdout.write(f"Accessing file '{filepath}'\n")

    content = ""
    try:
        f = open(filepath, "r")
        try:
            content = f.read()
            sys.stdout.write(content)
        finally:
            f.close()
            sys.stdout.write(f"File '{filepath}' closed.\n")
    except Exception as e:
        sys.stderr.write(f"[STDERR] Error opening file '{filepath}': {e}\n")
        return

    sys.stdout.write("\nTransform data:\n")
    lines = content.splitlines()
    transformed_lines = [f"{line}#" for line in lines]
    transformed_content = "\n".join(transformed_lines)
    if transformed_lines:
        transformed_content += "\n"

    sys.stdout.write(transformed_content)

    sys.stdout.write("Enter new file name (or empty): ")
    sys.stdout.flush()
    out_name = sys.stdin.readline().strip()

    if not out_name:
        sys.stdout.write("Not saving data.\n")
        return

    sys.stdout.write(f"Saving data to '{out_name}'\n")
    try:
        out_file = open(out_name, "w")
        try:
            out_file.write(transformed_content)
            sys.stdout.write(f"Data saved in file '{out_name}'.\n")
        finally:
            out_file.close()
    except Exception as e:
        sys.stderr.write(f"[STDERR] Error opening file '{out_name}': {e}\n")
        sys.stdout.write("Data not saved.\n")


if __name__ == "__main__":
    main()

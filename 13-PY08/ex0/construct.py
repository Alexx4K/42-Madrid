#!/usr/bin/env python3

import os
import site
import sys


def is_venv() -> bool:
    return (
        sys.prefix != sys.base_prefix
        or hasattr(sys, "real_prefix")
        or "VIRTUAL_ENV" in os.environ
    )


def main() -> None:
    if not is_venv():
        print("Outside the Matrix")
        print("MATRIX STATUS: You're still plugged in")
        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")
        print("\nWARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:")
        print("python -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate # On Windows\n")
        print("Then run this program again.")
    else:
        env_path = sys.prefix
        env_name = os.path.basename(env_path)
        site_pkgs = site.getsitepackages()
        pkg_path = site_pkgs[0] if site_pkgs else "Unknown"

        print("Inside the Construct")
        print("MATRIX STATUS: Welcome to the construct")
        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {env_name}")
        print(f"Environment Path: {env_path}")
        print("\nSUCCESS: You're in an isolated environment!")
        print(
            "Safe to install packages without affecting "
            "the global system.\n"
        )
        print(f"Package installation path:\n{pkg_path}")


if __name__ == "__main__":
    main()

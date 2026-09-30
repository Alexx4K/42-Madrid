# This file fails mypy on purpose: alchemy.create_earth does not
# exist on the alchemy module interface (see alchemy/__init__.py),
# so accessing it is both a mypy error and a runtime AttributeError.
import alchemy


def main() -> None:
    print("=== Alembic 4 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print(f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth: ", end="")
    print(alchemy.create_earth())


if __name__ == "__main__":
    main()

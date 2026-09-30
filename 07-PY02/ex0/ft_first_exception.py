#!/usr/bin/env python3


def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    for item in ["25", "abc"]:
        print(f"Input data is '{item}'")
        try:
            temp = input_temperature(item)
            print(f"Temperature is now {temp}°C")
        except Exception as e:
            print(f"Caught input_temperature error: {e}")
    print("All tests completed - program didn't crash!")


def main() -> None:
    test_temperature()


if __name__ == "__main__":
    main()

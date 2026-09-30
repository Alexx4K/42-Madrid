from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    name: str = "Data Processor"

    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._next_rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        return self._storage.pop(0)

    def _store(self, value: str) -> None:
        self._storage.append((self._next_rank, value))
        self._next_rank += 1

    @property
    def total_processed(self) -> int:
        return self._next_rank

    def __len__(self) -> int:
        return len(self._storage)


class NumericProcessor(DataProcessor):

    name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(item, (int, float)) for item in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):

    name = "Text Processor"

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):

    name = "Log Processor"

    def validate(self, data: Any) -> bool:
        if self._is_log_entry(data):
            return True
        if isinstance(data, list):
            return all(self._is_log_entry(item) for item in data)
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            level = entry.get("log_level", "")
            message = entry.get("log_message", "")
            self._store(f"{level}: {message}")

    @staticmethod
    def _is_log_entry(data: Any) -> bool:
        if not isinstance(data, dict):
            return False
        for key, value in data.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
        return True


def demo_numeric() -> None:
    print("Testing Numeric Processor...")
    proc = NumericProcessor()
    print(f" Trying to validate input '42': {proc.validate(42)}")
    print(f" Trying to validate input 'Hello': {proc.validate('Hello')}")

    print(
        " Test invalid ingestion of string 'foo' without prior "
        "validation:"
    )
    try:
        proc.ingest("foo")
    except ValueError as error:
        print(f" Got exception: {error}")

    data: list[int | float] = [1, 2, 3, 4, 5]
    print(f" Processing data: {data}")
    proc.ingest(data)
    print(" Extracting 3 values...")
    for i in range(3):
        _, value = proc.output()
        print(f" Numeric value {i}: {value}")


def demo_text() -> None:
    print("\nTesting Text Processor...")
    proc = TextProcessor()
    print(f" Trying to validate input '42': {proc.validate(42)}")

    data = ["Hello", "Nexus", "World"]
    print(f" Processing data: {data}")
    proc.ingest(data)
    print(" Extracting 1 value...")
    _, value = proc.output()
    print(f" Text value 0: {value}")


def demo_log() -> None:
    print("\nTesting Log Processor...")
    proc = LogProcessor()
    print(f" Trying to validate input 'Hello': {proc.validate('Hello')}")

    data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f" Processing data: {data}")
    proc.ingest(data)
    print(" Extracting 2 values...")
    for i in range(2):
        _, value = proc.output()
        print(f" Log entry {i}: {value}")


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")
    demo_numeric()
    demo_text()
    demo_log()


if __name__ == "__main__":
    main()

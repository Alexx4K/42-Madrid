#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._buffer: list[tuple[int, str]] = []
        self._total_processed: int = 0
        self._current_rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._buffer:
            raise IndexError("No data available to output")
        return self._buffer.pop(0)

    def get_stats(self) -> tuple[int, int]:
        return (self._total_processed, len(self._buffer))


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        if isinstance(data, list):
            if not data:
                return False
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._buffer.append((self._current_rank, str(item)))
            self._current_rank += 1
            self._total_processed += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            if not data:
                return False
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            self._buffer.append((self._current_rank, item))
            self._current_rank += 1
            self._total_processed += 1


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        def is_log_dict(d: Any) -> bool:
            if not isinstance(d, dict):
                return False
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in d.items()
            )

        if is_log_dict(data):
            return True
        if isinstance(data, list):
            if not data:
                return False
            return all(is_log_dict(x) for x in data)
        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        items = data if isinstance(data, list) else [data]
        for item in items:
            if "log_level" in item and "log_message" in item:
                formatted = f"{item['log_level']}: {item['log_message']}"
            else:
                formatted = ": ".join(item.values())
            self._buffer.append((self._current_rank, formatted))
            self._current_rank += 1
            self._total_processed += 1


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for elem in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(elem):
                    proc.ingest(elem)
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error - Can't process element in stream: "
                    f"{elem}"
                )

    def print_processors_stats(self) -> None:
        print("=== DataStream statistics ===")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            total, remaining = proc.get_stats()
            name = proc.__class__.__name__.replace(
                "Processor", " Processor"
            )
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus Data Stream ===")
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()

    print("Registering Numeric Processor")
    ds.register_processor(np)

    batch1: list[Any] = [
        "Hello world",
        [3.14, 1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]

    print(f"Send first batch of data on stream: {batch1}")
    ds.process_stream(batch1)
    ds.print_processors_stats()

    print("Registering other data processors")
    ds.register_processor(tp)
    ds.register_processor(lp)

    print("Send the same batch again")
    ds.process_stream(batch1)
    ds.print_processors_stats()

    print(
        "Consume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        np.output()
    for _ in range(2):
        tp.output()
    for _ in range(1):
        lp.output()

    ds.print_processors_stats()


if __name__ == "__main__":
    main()

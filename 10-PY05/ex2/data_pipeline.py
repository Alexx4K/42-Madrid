#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Protocol


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

    def has_data(self) -> bool:
        return len(self._buffer) > 0


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


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        vals = [v for _, v in data]
        print("CSV Output:")
        print(", ".join(vals))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return
        items = [f'"item_{rank}": "{val}"' for rank, val in data]
        print("JSON Output:")
        print("{" + ", ".join(items) + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            extracted: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.has_data():
                    extracted.append(proc.output())
            if extracted:
                plugin.process_output(extracted)

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
    print("=== Code Nexus Data Pipeline ===")
    print("Initialize Data Stream...")
    ds = DataStream()
    ds.print_processors_stats()

    np = NumericProcessor()
    tp = TextProcessor()
    lp = LogProcessor()

    print("Registering Processors")
    ds.register_processor(np)
    ds.register_processor(tp)
    ds.register_processor(lp)

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

    csv_plugin = CSVExportPlugin()
    json_plugin = JSONExportPlugin()

    print("Send 3 processed data from each processor to a CSV plugin:")
    ds.output_pipeline(3, csv_plugin)
    ds.print_processors_stats()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]

    print("Send another batch of data:")
    ds.process_stream(batch2)
    ds.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    ds.output_pipeline(5, json_plugin)
    ds.print_processors_stats()


if __name__ == "__main__":
    main()

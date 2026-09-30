#!/usr/bin/env python3

import random
from typing import Generator

PLAYERS = ["alice", "bob", "charlie", "dylan"]
ACTIONS = [
    "run",
    "eat",
    "sleep",
    "grab",
    "move",
    "climb",
    "swim",
    "use",
    "release",
]


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        yield (random.choice(PLAYERS), random.choice(ACTIONS))


def consume_event(
    events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while events:
        idx = random.randint(0, len(events) - 1)
        item = events.pop(idx)
        yield item


def main() -> None:
    print("=== Game Data Stream Processor ===")
    stream = gen_event()
    for i in range(1000):
        p, a = next(stream)
        print(f"Event {i}: Player {p} did action {a}")

    event_list = [next(gen_event()) for _ in range(10)]
    print(f"Built list of 10 events: {event_list}")

    for event in consume_event(event_list):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {event_list}")


if __name__ == "__main__":
    main()

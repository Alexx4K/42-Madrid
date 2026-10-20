#!/usr/bin/env python3

from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name: str = name
        self.type: str = creature_type

    def describe(self) -> str:
        return f"{self.name} is a {self.type} type Creature"

    @abstractmethod
    def attack(self) -> str:
        pass


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass

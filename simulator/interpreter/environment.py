from dataclasses import dataclass
from typing import Self

from simulator.interpreter.types import ArduinoType
from simulator.interpreter.token import Token


@dataclass
class Value:
    value_type: ArduinoType
    value: object


class Environment:
    """
    Storage for variables and their values.

    An environment can have an enclosing environment. This forms a tree
    structure where each scope has an environment where its variables can live
    in.
    """

    values: dict[str, Value | None]
    enclosing: Self | None

    def __init__(self, enclosing: Self | None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: Token, value: Value | None):
        """
        Defines a variable by its `name` and `value`.

        If a variable should be defined but not initialized, use `None` as the
        `value`.
        """

        # this should not happen, checked in the Resolver
        assert name not in self.values

        self.values[name.lexeme] = value

    def assign(self, name: Token, value: Value | None):
        if name in self.values:
            self.values[name.lexeme] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        # should be unreachable, checked in the Resolver
        return None


    def get(self, name: Token) -> Value | None:
        if name in self.values:
            return self.values[name.lexeme]

        if self.enclosing:
            return self.enclosing.get(name)

        # should be unreachable, checked in the Resolver
        return None

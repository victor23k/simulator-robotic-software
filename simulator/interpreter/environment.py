from __future__ import annotations

from typing import override, Self
from dataclasses import dataclass

from simulator.interpreter.sema.types import (
    ArduinoType,
    coerce_value,
)


@dataclass
class Value:
    value_type: ArduinoType
    value: object

    def coerce(self, arduino_type: ArduinoType):
        self.value_type = arduino_type
        self.value = coerce_value(self.value_type, self.value)

    @override
    def __eq__(self, value: object, /) -> bool:
        return (
            isinstance(value, Value)
            and self.value_type is value.value_type
            and self.value == value.value
        )


class Environment:
    """
    Storage for variables and their values.

    An environment can have an enclosing environment. This forms a tree
    structure where each scope has an environment where its variables can live
    in.

    Values stored in an environment can be of type Value, Function or LibFn.
    """

    values: dict[str, Value]
    enclosing: Self | None

    def __init__(self, enclosing: Self | None):
        self.values = {}
        self.enclosing = enclosing
        self.non_modifiable = set()

    @override
    def __repr__(self) -> str:
        return f"Environment=(values={self.values}, enclosing={self.enclosing})"

    def define(self, name: str, value: Value | None):
        """
        Defines a variable by its `name` and `value`.

        If a variable should be defined but not initialized, use `None` as the
        `value`.
        """

        # this should not happen, checked in the Resolver
        assert name not in self.values

        # if shadowing is not allowed, use depth to get the env to define
        self.values[name] = value

    def assign(self, name: str, value: Value):
        if name in self.values:
            self.values[name] = value
            return

        if self.enclosing:
            self.enclosing.assign(name, value)
            return

        # should be unreachable, checked in the Resolver
        return None

    def get(self, name: str, distance: int) -> Value | None:
        env = self._ancestor(distance)

        if name in env.values:
            return env.values[name]
        else:
            # unreachable if resolver is good
            pass

    def _ancestor(self, distance: int) -> Self:
        while distance > 0 and self.enclosing:
            return self.enclosing._ancestor(distance - 1)

        return self

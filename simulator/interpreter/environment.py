from enum import Enum
from dataclasses import dataclass
from simulator.interpreter.token import Token, TokenType


class EnvError(Enum):
    Redefinition = 1
    VariableDoesNotExist = 2


@dataclass
class Value:
    value_type: TokenType
    value: object


class Environment:
    """
    Storage for variables and their values.
    """

    values: dict[str, Value]

    def __init__(self):
        self.values = {}

    def define(self, name: Token, value: Value) -> None | EnvError:
        if name in self.values:
            return EnvError.Redefinition

        self.values[name.lexeme] = value

    def set(self, name: Token, value: Value) -> None | EnvError:
        if name not in self.values:
            return EnvError.VariableDoesNotExist

        self.values[name.lexeme] = value

    def get(self, name: Token) -> Value | EnvError:
        if name not in self.values:
            return EnvError.VariableDoesNotExist

        return self.values[name.lexeme]

from typing import Self
from enum import Enum

from simulator.interpreter.lex.token import TokenType

class PrecLevel(Enum):
    UNKNOWN = 0
    MINIMAL = 1
    LOGICAL_OR = 2
    LOGICAL_AND = 3
    BITWISE_OR = 4
    BITWISE_XOR = 5
    BITWISE_AND = 6
    EQUALITY = 7
    RELATIONAL = 8
    SHIFT = 9
    ADDITIVE = 10
    MULTIPLICATIVE = 11

    def __gt__(self, other: Self) -> bool:
        return self.value > other.value

    def __lt__(self, other: Self) -> bool:
        return self.value < other.value

    def __ge__(self, other: Self) -> bool:
        return self.value >= other.value

    def __le__(self, other: Self) -> bool:
        return self.value <= other.value

    def __add__(self, num: int) -> Self:
        return PrecLevel(self.value + num)

    def __radd__(self, num: int) -> Self:
        return PrecLevel(self.value + num)


binary_op_precedence = {
    TokenType.EQUAL: PrecLevel.MINIMAL,
    TokenType.PLUS_EQUAL: PrecLevel.MINIMAL,
    TokenType.MINUS_EQUAL: PrecLevel.MINIMAL,
    TokenType.STAR_EQUAL: PrecLevel.MINIMAL,
    TokenType.SLASH_EQUAL: PrecLevel.MINIMAL,
    TokenType.PERCENTAGE_EQUAL: PrecLevel.MINIMAL,
    TokenType.AND_EQUAL: PrecLevel.MINIMAL,
    TokenType.OR_EQUAL: PrecLevel.MINIMAL,
    TokenType.XOR_EQUAL: PrecLevel.MINIMAL,

    TokenType.LOGICAL_OR: PrecLevel.LOGICAL_OR,
    TokenType.LOGICAL_AND: PrecLevel.LOGICAL_AND,

    TokenType.BITWISE_OR: PrecLevel.BITWISE_OR,
    TokenType.BITWISE_XOR: PrecLevel.BITWISE_XOR,
    TokenType.AMPERSAND: PrecLevel.BITWISE_AND,

    TokenType.EQUAL_EQUAL: PrecLevel.EQUALITY,
    TokenType.NOT_EQUAL: PrecLevel.EQUALITY,

    TokenType.LESS_THAN: PrecLevel.RELATIONAL,
    TokenType.LESS_THAN_EQUAL: PrecLevel.RELATIONAL,
    TokenType.GREATER_THAN: PrecLevel.RELATIONAL,
    TokenType.GREATER_THAN_EQUAL: PrecLevel.RELATIONAL,

    TokenType.BITSHIFT_LEFT: PrecLevel.SHIFT,
    TokenType.BITSHIFT_RIGHT: PrecLevel.SHIFT,

    TokenType.PLUS: PrecLevel.ADDITIVE,
    TokenType.MINUS: PrecLevel.ADDITIVE,

    TokenType.STAR: PrecLevel.MULTIPLICATIVE,
    TokenType.SLASH: PrecLevel.MULTIPLICATIVE,
    TokenType.PERCENTAGE: PrecLevel.MULTIPLICATIVE,
}

def get_binary_op_precedence(token_type: TokenType) -> PrecLevel:
    return binary_op_precedence.get(token_type, PrecLevel.UNKNOWN)

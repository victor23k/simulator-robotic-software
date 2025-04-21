from typing import Self
from enum import Enum
from simulator.interpreter.token import TokenType

class PrecLevel(Enum):
    UNKNOWN = 0
    MINIMAL = 1
    ADDITIVE = 2
    MULTIPLICATIVE = 3

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


def get_binary_op_precedence(token_type: TokenType) -> PrecLevel:
    match token_type:
        case TokenType.PLUS | TokenType.MINUS:
            return PrecLevel.ADDITIVE
        case TokenType.STAR | TokenType.SLASH | TokenType.PERCENTAGE:
            return PrecLevel.MULTIPLICATIVE
        case _:
            return PrecLevel.UNKNOWN

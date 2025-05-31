from enum import Enum
from simulator.interpreter.token import TokenType


class Assoc(Enum):
    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2


def get_binary_op_assoc(token_type: TokenType) -> Assoc:
    match token_type:
        case (
            TokenType.PLUS
            | TokenType.MINUS
            | TokenType.STAR
            | TokenType.SLASH
            | TokenType.PERCENTAGE
            | TokenType.EQUAL_EQUAL
            | TokenType.NOT_EQUAL
            | TokenType.LESS_THAN
            | TokenType.LESS_THAN_EQUAL
            | TokenType.GREATER_THAN
            | TokenType.GREATER_THAN_EQUAL
            | TokenType.BITSHIFT_LEFT
            | TokenType.BITSHIFT_RIGHT
            | TokenType.AMPERSAND
            | TokenType.BITWISE_OR
            | TokenType.BITWISE_XOR
            | TokenType.LOGICAL_AND
            | TokenType.LOGICAL_OR
        ):
            return Assoc.LEFT
        case (
            TokenType.EQUAL
            | TokenType.PLUS_EQUAL
            | TokenType.MINUS_EQUAL
            | TokenType.STAR_EQUAL
            | TokenType.SLASH_EQUAL
            | TokenType.PERCENTAGE_EQUAL
            | TokenType.AND_EQUAL
            | TokenType.OR_EQUAL
            | TokenType.XOR_EQUAL
        ):
            return Assoc.RIGHT
        case _:
            return Assoc.UNKNOWN

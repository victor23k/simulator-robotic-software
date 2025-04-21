from enum import Enum
from simulator.interpreter.token import TokenType

class Assoc(Enum):
    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2

def get_binary_op_assoc(token_type: TokenType) -> Assoc:
    match token_type:
        case TokenType.PLUS | TokenType.MINUS | TokenType.STAR | TokenType.SLASH:
            return Assoc.LEFT
        case _:
            return Assoc.UNKNOWN

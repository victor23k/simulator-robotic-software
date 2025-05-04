from dataclasses import dataclass
from enum import Enum

from simulator.interpreter.token import Token, TokenType


class ArduinoBuiltinType(Enum):
    INT = 1
    FLOAT = 2
    DOUBLE = 3

    NONE = 30


@dataclass
class ArduinoObjType:
    classname: str


type ArduinoType = ArduinoBuiltinType | ArduinoObjType

class TypeException(Exception):
    pass

def token_to_arduino_type(token: Token) -> ArduinoType:
    match token.token:
        case TokenType.INT | TokenType.INT_LITERAL:
            return ArduinoBuiltinType.INT
        case TokenType.FLOAT | TokenType.FLOAT_LITERAL:
            return ArduinoBuiltinType.FLOAT
        case TokenType.DOUBLE:
            return ArduinoBuiltinType.DOUBLE
        case TokenType.IDENTIFIER:
            return ArduinoObjType(token.lexeme)
        case _:
            return ArduinoObjType(token.lexeme)

from dataclasses import dataclass
from enum import Enum

from simulator.interpreter.token import Token, TokenType

class ArduinoBuiltinType(Enum):
    ERR = 0
    INT = 1
    FLOAT = 2
    DOUBLE = 3

    BOOL = 4

type ArduinoType = ArduinoBuiltinType | ArduinoObjType

@dataclass
class ArduinoObjType:
    classname: str

def token_to_arduino_type(token: Token) -> ArduinoType:
    match token.token:
        case TokenType.INT | TokenType.INT_LITERAL:
            return ArduinoBuiltinType.INT
        case TokenType.FLOAT | TokenType.FLOAT_LITERAL:
            return ArduinoBuiltinType.FLOAT
        case TokenType.DOUBLE:
            return ArduinoBuiltinType.DOUBLE
        case TokenType.BOOL | TokenType.TRUE | TokenType.FALSE:
            return ArduinoBuiltinType.BOOL
        case TokenType.IDENTIFIER:
            return ArduinoObjType(token.lexeme)
        case _:
            return ArduinoObjType(token.lexeme)

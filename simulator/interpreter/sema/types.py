from dataclasses import dataclass
from enum import Enum

from simulator.interpreter.lex.token import Token, TokenType


class ArduinoBuiltinType(Enum):
    ERR = 0

    BOOL = 1
    CHAR = 2
    UNSIGNED_CHAR = 3
    INT = 4
    UNSIGNED_INT = 5
    LONG = 6
    UNSIGNED_LONG = 7
    FLOAT = 8
    DOUBLE = 9

    VOID = 10


type ArduinoType = ArduinoBuiltinType | ArduinoObjType | None


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


def types_compatibility(type_a: ArduinoType, type_b: ArduinoType) -> bool:
    return type_a == type_b or (
        type_a
        in [
            ArduinoBuiltinType.INT,
            ArduinoBuiltinType.FLOAT,
            ArduinoBuiltinType.DOUBLE,
        ]
        and type_b
        in [
            ArduinoBuiltinType.INT,
            ArduinoBuiltinType.FLOAT,
            ArduinoBuiltinType.DOUBLE,
        ]
    )


def coerce_types(type_a: ArduinoType, type_b: ArduinoType) -> ArduinoType:
    if type_a == type_b:
        return type_a
    elif type_b in [
        ArduinoBuiltinType.INT,
        ArduinoBuiltinType.FLOAT,
        ArduinoBuiltinType.DOUBLE,
    ]:
        return type_a

    return ArduinoBuiltinType.ERR


def type_from_specifier_list(specifiers: list[Token]):
    return next(filter(lambda spec: spec.is_var_type(), specifiers))


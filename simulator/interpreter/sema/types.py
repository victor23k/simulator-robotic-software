from dataclasses import dataclass
from enum import Enum
from typing import override

from simulator.interpreter.lex.token import Token, TokenType

type ArduinoType = ArduinoArray | ArduinoBuiltinType | ArduinoObjType | None


class ArduinoBuiltinType(Enum):
    ERR = 0

    BOOL = 1
    CHAR = 2
    UNSIGNED_CHAR = 3
    SHORT = 4 
    INT = 5
    UNSIGNED_INT = 6
    LONG = 7
    UNSIGNED_LONG = 8
    FLOAT = 9
    DOUBLE = 10

    VOID = 11


@dataclass
class ArduinoArray:
    ttype: ArduinoType

    @override
    def __eq__(self, value: object, /) -> bool:
        return (isinstance(value, ArduinoArray) and self.ttype == value.ttype) 

    @override
    def __hash__(self) -> int:
        return self.ttype.__hash__()


@dataclass
class ArduinoObjType:
    classname: str


def token_to_arduino_type(token: Token) -> ArduinoType:
    match token.token:
        case TokenType.INT | TokenType.INT_LITERAL:
            return ArduinoBuiltinType.INT
        case TokenType.FLOAT | TokenType.FLOAT_LITERAL:
            return ArduinoBuiltinType.FLOAT
        case TokenType.CHAR | TokenType.CHAR_LITERAL:
            return ArduinoBuiltinType.CHAR
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
    try:
        return next(filter(lambda spec: spec.is_var_type(), specifiers))
    except StopIteration:
        ArduinoBuiltinType.ERR

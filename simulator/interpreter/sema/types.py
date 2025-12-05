from dataclasses import dataclass
from enum import Enum
from typing import override

from simulator.interpreter.lex.token import Token, TokenType

type ArduinoType = ArduinoArray | ArduinoBuiltinType | ArduinoObjType | None


class ArduinoBuiltinType(Enum):
    ERR = 0

    BOOL = 1
    BYTE = 2
    CHAR = 3
    UNSIGNED_CHAR = 4
    SHORT = 5
    INT = 6
    UNSIGNED_INT = 7
    LONG = 8
    UNSIGNED_LONG = 9
    FLOAT = 10
    DOUBLE = 11

    VOID = 12


@dataclass
class ArduinoArray:
    ttype: ArduinoType

    @override
    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, ArduinoArray) and self.ttype == value.ttype

    @override
    def __hash__(self) -> int:
        return self.ttype.__hash__()


@dataclass
class ArduinoObjType:
    classname: str


def str_to_arduino_type(type_name: str) -> ArduinoType:
    match type_name:
        case "int":
            return ArduinoBuiltinType.INT
        case "uint":
            return ArduinoBuiltinType.UNSIGNED_INT
        case "float":
            return ArduinoBuiltinType.FLOAT
        case "char":
            return ArduinoBuiltinType.CHAR
        case "double":
            return ArduinoBuiltinType.DOUBLE
        case "bool":
            return ArduinoBuiltinType.BOOL
        case "byte":
            return ArduinoBuiltinType.BYTE
        case _:
            return ArduinoObjType(type_name)


def token_to_arduino_type(token: Token) -> ArduinoType:
    match token.token:
        case TokenType.INT | TokenType.INT_LITERAL:
            return ArduinoBuiltinType.INT
        case TokenType.FLOAT | TokenType.FLOAT_LITERAL:
            return ArduinoBuiltinType.FLOAT
        case TokenType.CHAR | TokenType.CHAR_LITERAL:
            return ArduinoBuiltinType.CHAR
        case TokenType.STRING_LITERAL:
            return ArduinoObjType("String")
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


def type_from_specifier_list(specifiers: list[Token]) -> Token | None:
    try:
        return next(filter(lambda spec: spec.is_var_type(), specifiers))
    except StopIteration:
        return None

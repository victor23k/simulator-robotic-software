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

    @override
    def __str__(self) -> str:
        return self.name

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __le__(self, other) -> bool:
        return self.value <= other.value

@dataclass
class ArduinoArray:
    ttype: ArduinoType

    @override
    def __eq__(self, value: object, /) -> bool:
        return isinstance(value, ArduinoArray) and self.ttype == value.ttype

    @override
    def __hash__(self) -> int:
        return self.ttype.__hash__()

    @override
    def __str__(self) -> str:
        return f"{self.ttype}[]"

@dataclass
class ArduinoObjType:
    classname: str

    @override
    def __str__(self) -> str:
        return self.classname

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
        case (TokenType.INT | TokenType.INT_LITERAL | TokenType.INPUT |
            TokenType.OUTPUT | TokenType.HIGH | TokenType.LOW |
            TokenType.ANALOG_PIN):
            return ArduinoBuiltinType.INT
        case TokenType.BYTE:
            return ArduinoBuiltinType.BYTE
        case TokenType.UNSIGNED_CHAR:
                return ArduinoBuiltinType.UNSIGNED_CHAR
        case TokenType.SHORT:
                return ArduinoBuiltinType.SHORT
        case TokenType.UNSIGNED_INT:
                return ArduinoBuiltinType.UNSIGNED_INT
        case TokenType.LONG:
                return ArduinoBuiltinType.LONG
        case TokenType.UNSIGNED_LONG:
                return ArduinoBuiltinType.UNSIGNED_LONG
        case TokenType.FLOAT | TokenType.FLOAT_LITERAL:
            return ArduinoBuiltinType.FLOAT
        case TokenType.CHAR | TokenType.CHAR_LITERAL:
            return ArduinoBuiltinType.CHAR
        case TokenType.STRING_LITERAL:
            return ArduinoObjType("String")
        case TokenType.DOUBLE:
            return ArduinoBuiltinType.DOUBLE
        case TokenType.BOOL | TokenType.BOOLEAN | TokenType.TRUE | TokenType.FALSE:
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
    ) or (
        isinstance(type_a, ArduinoBuiltinType)
        and isinstance(type_b, ArduinoBuiltinType) 
        and type_a >= ArduinoBuiltinType.BOOL
        and type_a <= ArduinoBuiltinType.UNSIGNED_LONG
        and type_b >= ArduinoBuiltinType.BOOL
        and type_b <= ArduinoBuiltinType.UNSIGNED_LONG
    ) or (
        type_a == ArduinoArray(ArduinoBuiltinType.CHAR) and
        type_b == ArduinoObjType("String")
    ) or (
        type_b == ArduinoArray(ArduinoBuiltinType.CHAR) and
        type_a == ArduinoObjType("String")
    )


def coerce_types(type_a: ArduinoType, type_b: ArduinoType) -> ArduinoType:
    if type_a == type_b:
        return type_a
    elif (
        type_b == ArduinoArray(ArduinoBuiltinType.CHAR) and
        type_a == ArduinoObjType("String")
    ):
        return type_a
    elif (
        isinstance(type_a, ArduinoBuiltinType)
        and isinstance(type_b, ArduinoBuiltinType) 
        and ArduinoBuiltinType.BOOL <= type_a <= ArduinoBuiltinType.DOUBLE
        and ArduinoBuiltinType.BOOL <= type_b <= ArduinoBuiltinType.DOUBLE
    ):
        return max(type_a, type_b)

    return type_a


def coerce_value(arduino_type: ArduinoType, value: object) -> object:
    match arduino_type:
        case ArduinoBuiltinType.CHAR:
            return value
        case ArduinoBuiltinType() if ArduinoBuiltinType.BOOL <= arduino_type <= ArduinoBuiltinType.UNSIGNED_LONG:
            if value == 'LOW':
                return 0
            elif value == 'HIGH':
                return 1
            elif type(value) is str:
                return ord(value)
            else:
                return int(value)
        case ArduinoBuiltinType.FLOAT | ArduinoBuiltinType.DOUBLE:
            return float(value)
        case ArduinoBuiltinType.BOOL:
            return bool(value)
        case _:
            return value


def type_from_specifier_list(specifiers: list[Token]) -> Token | None:
    try:
        return next(filter(lambda spec: spec.is_var_type(), specifiers))
    except StopIteration:
        return None

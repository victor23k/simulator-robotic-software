from dataclasses import dataclass
from enum import Enum


class TokenType(Enum):
    PLUS = 1
    EQUAL = 2
    SLASH = 3
    STAR = 4
    PERCENTAGE = 5
    MINUS = 6
    AMPERSAND = 7
    EQUAL_EQUAL = 8
    GREATER_THAN = 9
    GREATER_THAN_EQUAL = 10
    LESS_THAN = 11
    LESS_THAN_EQUAL = 12
    NOT_EQUAL = 13

    BITSHIFT_LEFT = 14
    BITSHIFT_RIGHT = 15
    BITWISE_NOT = 16
    BITWISE_OR = 17
    BITWISE_XOR = 18

    BLOCK_COMMENT_START = 19
    BLOCK_COMMENT_END = 20
    LEFT_BRACE = 21
    RIGHT_BRACE = 22
    DEFINE = 23
    INCLUDE = 24
    SEMICOLON = 25
    LINE_COMMENT = 26

    LOGICAL_AND = 27
    LOGICAL_NOT = 28
    LOGICAL_OR = 29

    PLUS_EQUAL = 30
    AND_EQUAL = 31
    OR_EQUAL = 32
    XOR_EQUAL = 33
    SLASH_EQUAL = 34
    STAR_EQUAL = 35
    PERCENTAGE_EQUAL = 36
    MINUS_EQUAL = 37
    DECREMENT = 38
    INCREMENT = 39

    # variable qualifiers
    CONST = 40
    STATIC = 41
    VOLATILE = 42

    # constants
    HIGH = 50
    LOW = 51
    INPUT = 52
    INPUT_PULLUP = 53
    OUTPUT = 54
    LED_BUILTIN = 55
    TRUE = 56
    FALSE = 57

    # data types
    BOOL = 60
    BOOLEAN = 61
    BYTE = 62
    CHAR = 43
    DOUBLE = 64
    FLOAT = 65
    INT = 66
    LONG = 67
    SHORT = 68
    SIZE_T = 69
    UNSIGNED_INT = 70
    UNSIGNED_CHAR = 71
    UNSIGNED_LONG = 72
    VOID = 73
    WORD = 74

    # control structures
    BREAK = 80
    CASE = 81
    CONTINUE = 82
    DO = 83
    ELSE = 84
    FOR = 85
    GOTO = 86
    IF = 87
    RETURN = 88
    SWITCH = 89
    WHILE = 90
    DEFAULT = 91

    LEFT_PAREN = 92
    RIGHT_PAREN = 93
    LEFT_BRACKET = 94
    RIGHT_BRACKET = 95
    DOT = 96
    COMMA = 97
    NUMBER = 98
    IDENTIFIER = 99

    EOF = 100
    ERROR = 101

    # numeric literals
    FLOAT_LITERAL = 110
    INT_LITERAL = 111

    COLON = 112


@dataclass
class Token:
    """Arduino Language token."""

    token: TokenType
    lexeme: str
    literal: object
    line: int
    column: int

    def is_boolean(self) -> bool:
        return self.token in [
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS_THAN,
            TokenType.LESS_THAN_EQUAL,
            TokenType.GREATER_THAN,
            TokenType.GREATER_THAN_EQUAL,
            TokenType.LOGICAL_AND,
            TokenType.LOGICAL_OR,
        ]

    def is_binary(self) -> bool:
        return self.token in [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENTAGE,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.LESS_THAN,
            TokenType.LESS_THAN_EQUAL,
            TokenType.GREATER_THAN,
            TokenType.GREATER_THAN_EQUAL,
            TokenType.AMPERSAND,
            TokenType.BITWISE_OR,
            TokenType.BITWISE_XOR,
            TokenType.BITSHIFT_LEFT,
            TokenType.BITSHIFT_RIGHT,
            TokenType.LOGICAL_AND,
            TokenType.LOGICAL_OR,
            TokenType.EQUAL,
            TokenType.PLUS_EQUAL,
            TokenType.MINUS_EQUAL,
            TokenType.STAR_EQUAL,
            TokenType.SLASH_EQUAL,
            TokenType.PERCENTAGE_EQUAL,
            TokenType.AND_EQUAL,
            TokenType.OR_EQUAL,
            TokenType.XOR_EQUAL,
        ]
    
    def is_var_type(self) -> bool:
        return self.token in [
            TokenType.BOOL,
            TokenType.BOOLEAN,
            TokenType.BYTE,
            TokenType.CHAR,
            TokenType.DOUBLE,
            TokenType.FLOAT,
            TokenType.INT,
            TokenType.LONG,
            TokenType.SHORT,
            TokenType.SIZE_T,
            TokenType.UNSIGNED_INT,
            TokenType.VOID,
            TokenType.WORD,
            TokenType.UNSIGNED_CHAR,
            TokenType.UNSIGNED_LONG,
        ]


    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += f"{' ' * (ntab + 2)}token_type={self.token},\n"
        result += f"{' ' * (ntab + 2)}lexeme={self.lexeme},\n"
        result += f"{' ' * (ntab + 2)}literal={self.literal},\n"
        result += f"{' ' * (ntab + 2)}line={self.line},\n"
        result += f"{' ' * (ntab + 2)}column={self.column},\n"
        result += f"{' ' * (ntab)})"

        return result

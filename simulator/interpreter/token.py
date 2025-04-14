from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    PLUS = 1
    EQUAL = 2
    SLASH = 3
    STAR = 4
    PERCENTAGE = 5
    DASH = 6
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
    DASH_EQUAL = 37
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
    INT = 65
    LONG = 66
    SHORT = 67
    SIZE_T = 68
    # STRING = 69 creo que esto es una clase que tengo que implementar
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

    LEFT_PAREN = 91
    RIGHT_PAREN = 92
    LEFT_BRACKET = 93
    RIGHT_BRACKET = 94
    DOT = 95
    NUMBER = 96
    IDENTIFIER = 97

    EOF = 100

@dataclass
class Token:
    """Arduino Language token."""
    token: TokenType
    lexeme: str
    literal: object
    line: int

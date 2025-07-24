from dataclasses import dataclass

from simulator.interpreter.lex.token import Token

def diagnostic_from_token(message: str, token: Token):
    return Diagnostic(message, token.line, token.column, len(token.lexeme) +
        token.column)

@dataclass
class Diagnostic:
    """
    Diagnostics about parsing errors with line and column information.
    """

    message: str
    line: int
    col_start: int
    col_end: int

class ArduinoRuntimeError(Exception):
    pass

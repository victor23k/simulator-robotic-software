from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from simulator.interpreter.lex.token import Token


def diagnostic_from_token(message: str, token: Token) -> Diagnostic:
    return Diagnostic(
        message, token.line, token.column, len(token.lexeme) + token.column
    )


def printable_diagnostics(diags: list[Diagnostic], code: str) -> str:
    return "\n" + str.join("\n", [diag.print(code) for diag in diags])


@dataclass
class Diagnostic:
    """
    Diagnostics about parsing errors with line and column information.
    """

    message: str
    line: int
    col_start: int
    col_end: int

    def print(self, code: str) -> str:
        return f"""{self.message}
Line {self.line}: {code.splitlines()[self.line - 1]}
{" " * len(f"Line {self.line}: ")}{" " * self.col_start}{"^" * (self.col_end - self.col_start)}
"""


class ArduinoRuntimeError(Exception):
    pass

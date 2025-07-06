from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from simulator.interpreter.stmt import Stmt

from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.environment import Environment

class Interpreter:
    """
    Runs an Arduino Language AST by evaluating expressions and executing
    statements.
    """

    environment: Environment
    globals: Environment
    diagnostics: list[Diagnostic]

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        self.globals = Environment(None)
        self.environment = self.globals

    def print_diagnostics(self, diagnostics: list[Diagnostic]):
        pass

    def run(self, statements: list[Stmt]) -> None:
        for statement in statements:
            statement.execute(self.environment)

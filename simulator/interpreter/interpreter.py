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

    statements: list[Stmt]
    environment: Environment
    globals: Environment = Environment(None)
    diagnostics: list[Diagnostic]

    def __init__(self, statements: list[Stmt], diagnostics: list[Diagnostic]):
        self.statements = statements
        self.diagnostics = diagnostics
        self.environment = self.globals

    def print_diagnostics(self, diagnostics: list[Diagnostic]):
        pass

    def run(self) -> None:
        for statement in self.statements:
            statement.execute(self.environment)

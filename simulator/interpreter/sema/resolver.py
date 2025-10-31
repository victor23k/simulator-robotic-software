from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from simulator.interpreter.ast.stmt import Stmt

from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.sema.scope import ScopeChain
from simulator.interpreter.sema.types import ArduinoType


class FunctionState(Enum):
    NONE = 1
    FUNCTION = 2


class FunctionType:
    fn_state: FunctionState
    return_type: ArduinoType

    def __init__(self):
        self.fn_state = FunctionState.NONE
        self.return_type = None


class Resolver:
    """
    Semantic analysis. Performs type checking and resolves the scopes for
    variables.
    """

    diagnostics: list[Diagnostic]
    scope_chain: ScopeChain
    function_type: FunctionType

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        self.scope_chain = ScopeChain(self.diagnostics)
        self.function_type = FunctionType()

    def resolve(self, statements: list[Stmt]):
        for statement in statements:
            statement.resolve(self.scope_chain, self.diagnostics,
                              self.function_type, False)

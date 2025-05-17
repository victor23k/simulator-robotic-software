from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.interpreter import Interpreter
from simulator.interpreter.scope import ScopeChain
from simulator.interpreter.stmt import Stmt


class Resolver:
    """
    This interpreter pass performs type checking and resolves the scopes for
    variables.
    """

    interpreter: Interpreter
    diagnostics: list[Diagnostic]
    scope_chain: ScopeChain

    def __init__(self, interpreter: Interpreter):
        self.diagnostics = interpreter.diagnostics
        self.scope_chain = ScopeChain(self.diagnostics, interpreter)
        self.interpreter = interpreter

    def resolve(self, stmts: list[Stmt]):
        for stmt in stmts:
            stmt.resolve(self.scope_chain, self.diagnostics)

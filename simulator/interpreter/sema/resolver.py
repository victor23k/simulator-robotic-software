from simulator.interpreter.ast.stmt import Stmt
from simulator.interpreter.diagnostic import Diagnostic
from simulator.interpreter.sema.scope import ScopeChain


class Resolver:
    """
    Semantic analysis. Performs type checking and resolves the scopes for
    variables.
    """

    diagnostics: list[Diagnostic]
    scope_chain: ScopeChain

    def __init__(self, diagnostics: list[Diagnostic]):
        self.diagnostics = diagnostics
        self.scope_chain = ScopeChain(self.diagnostics)

    def resolve(self, statements: list[Stmt]):
        for statement in statements:
            statement.resolve(self.scope_chain, self.diagnostics)

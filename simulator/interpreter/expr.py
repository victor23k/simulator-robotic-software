from dataclasses import dataclass
from typing import override

from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.token import Token

class Expr:
    """Expression in the Arduino Language"""
    pass

@dataclass
class BinaryExpr(Expr):
    lhs: Expr
    op: Token
    rhs: Expr

    @override
    def __repr__(self):
        return f"""{self.__class__.__name__}(
    op={self.op},
    lhs={repr(self.lhs).replace('\n', '\n    ')},
    rhs={repr(self.rhs).replace('\n', '\n    ')}
)"""

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return Diagnostic(message, self.op.line, self.op.column, self.op.column)

@dataclass()
class LiteralExpr(Expr):
    value: Token

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.value)

@dataclass
class VariableExpr(Expr):
    name: Token

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

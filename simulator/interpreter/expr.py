from dataclasses import dataclass
from simulator.interpreter.environment import Value
from simulator.interpreter.token import Token

class Expr:
    """Expression in the Arduino Language"""
    pass

@dataclass
class BinaryExpr(Expr):
    lhs: Expr
    op: Token
    rhs: Expr

    def __repr__(self):
        return f"""{self.__class__.__name__}(
    op={self.op},
    lhs={repr(self.lhs).replace('\n', '\n    ')},
    rhs={repr(self.rhs).replace('\n', '\n    ')}
)"""

class LiteralExpr(Expr):
    value: Value

    def __init__(self, token: Token):
        self.value = Value(token.token, token.literal)

@dataclass
class VariableExpr(Expr):
    name: Token

from dataclasses import dataclass
from simulator.interpreter.expr import Expr

class Stmt:
    """Arduino Statement"""
    pass

@dataclass
class ExpressionStmt(Stmt):
    expr: Expr

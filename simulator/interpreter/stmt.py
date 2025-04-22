from dataclasses import dataclass
from simulator.interpreter.expr import Expr
from simulator.interpreter.token import Token

class Stmt:
    """Arduino Statement"""
    pass

@dataclass
class ExpressionStmt(Stmt):
    expr: Expr

# declaration = type identifier [ array ] [ "=" expression ] ";"

# type = "bool"
#      | "boolean"
#      | "byte"
#      | "char"
#      | "double"
#      | "float"
#      | "int"
#      | "long"
#      | "short"
#      | "size_t"
#      | "unsigned char"
#      | "unsigned int"
#      | "unsigned long"
#      | "word"

# array = "[" number "]"


@dataclass
class VariableStmt(Stmt):
    var_type: Token
    name: Token
    initializer: Expr | None

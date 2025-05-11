from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:  # Only imports the below statements during type checking
    from simulator.interpreter.scope import ScopeChain

from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.environment import Environment
from simulator.interpreter.token import Token
from simulator.interpreter.types import ArduinoBuiltinType, ArduinoType, token_to_arduino_type

type Expr = BinaryExpr | VariableExpr | LiteralExpr

class BinaryExpr:
    lhs: Expr
    op: Token
    rhs: Expr
    ttype: ArduinoType | None

    op_table = {
        "*" : lambda x, y: x * y,
        "+" : lambda x, y: x + y,
        "-" : lambda x, y: x - y,
        "%" : lambda x, y: x % y,
    }

    def __init__(self, lhs: Expr, op: Token, rhs: Expr):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.ttype = None

    def to_string(self, ntab: int = 0) -> str:
        result: str = " "*ntab + str(self.op)
        result += self.lhs.to_string(ntab+2)
        result += self.rhs.to_string(ntab+2) + "\n"
        result += " "*ntab + str(self.ttype)
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return Diagnostic(message, self.op.line, self.op.column, self.op.column)

    def evaluate(self, env: Environment) -> object:
        left_value = self.lhs.evaluate(env)
        right_value = self.rhs.evaluate(env)
        result = self.op_table[self.op.lexeme](left_value, right_value)
        return result

    def check_type(self, scope_chain: ScopeChain):
        self.lhs.check_type(scope_chain)
        self.rhs.check_type(scope_chain)
        if self.lhs.ttype == self.rhs.ttype:
            self.ttype = self.lhs.ttype
        else:
            # add diag
            self.ttype = ArduinoBuiltinType.ERR 



class LiteralExpr:
    value: Token
    ttype: ArduinoType | None

    def __init__(self, token: Token):
        self.value = token
        self.ttype = None

    def evaluate(self, _env: Environment) -> object:
        return self.value.literal

    def to_string(self, ntab: int = 0) -> str:
        result: str = " "*ntab + str(self.value)
        result += " "*ntab + str(self.ttype)
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.value)

    def check_type(self, _scope_chain: ScopeChain):
        self.ttype = token_to_arduino_type(self.value)

class VariableExpr:
    name: Token
    ttype: ArduinoType | None
    scope_depth: int

    def __init__(self, token: Token):
        self.name = token
        self.ttype = None
        self.scope_depth = 0

    def evaluate(self, env: Environment) -> object:
        return env.get(self.name)

    def to_string(self, ntab: int = 0) -> str:
        result: str = " "*ntab + str(self.name)
        result += " "*ntab + str(self.ttype)
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def check_type(self, scope_chain: ScopeChain):
        self.ttype = scope_chain.get_type(self.name)

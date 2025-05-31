from __future__ import annotations

from typing import TYPE_CHECKING, override
if TYPE_CHECKING:
    from simulator.interpreter.scope import ScopeChain
    from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
    from simulator.interpreter.environment import Environment

from simulator.interpreter.environment import Value
from simulator.interpreter.token import Token
from simulator.interpreter.types import ArduinoBuiltinType, ArduinoType, token_to_arduino_type

type Expr = BinaryExpr | VariableExpr | LiteralExpr


class AssignExpr:
    name: Token
    value: Expr
    ttype: ArduinoType | None

    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value
        self.ttype = None

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.name.to_string(ntab+2, "name") + "\n"
        result += self.value.to_string(ntab+2, "value") + "\n"

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def evaluate(self, env: Environment) -> object:
        value_result = self.value.evaluate(env)

        env.assign(self.name.lexeme, Value(self.value.ttype, value_result))

        return value_result

    def check_type(self, scope_chain: ScopeChain, diags: list[Diagnostic]):
        self.value.check_type(scope_chain, diags)
        var_type = scope_chain.get_type(self.name)
        if var_type == self.value.ttype:
            self.ttype = var_type
        else:
            diag = diagnostic_from_token("Type of value assigned is not compatible with variable.", self.name)
            diags.append(diag)
            self.ttype = ArduinoBuiltinType.ERR 


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

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.lhs.to_string(ntab+2, "lhs") + "\n"
        result += self.op.to_string(ntab+2, "op") + "\n"
        result += self.rhs.to_string(ntab+2, "rhs") + "\n"

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return Diagnostic(message, self.op.line, self.op.column, self.op.column)

    def evaluate(self, env: Environment) -> object:
        left_value = self.lhs.evaluate(env)
        right_value = self.rhs.evaluate(env)
        result = self.op_table[self.op.lexeme](left_value, right_value)
        return result

    def check_type(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.lhs.check_type(scope_chain, diagnostics)
        self.rhs.check_type(scope_chain, diagnostics)
        if self.lhs.ttype == self.rhs.ttype:
            self.ttype = self.lhs.ttype
        else:
            diag = diagnostic_from_token("Types not compatible for this operation.", self.op)
            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR 


    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.lhs.resolve(scope_chain, diagnostics)
        self.rhs.resolve(scope_chain, diagnostics)
        self.check_type(scope_chain, diagnostics)


class LiteralExpr:
    value: Token
    ttype: ArduinoType | None

    def __init__(self, token: Token):
        self.value = token
        self.ttype = None

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.value.to_string(ntab+2, "value") + "\n"

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result

    def evaluate(self, _env: Environment) -> object:
        return self.value.literal

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.value)

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        self.ttype = token_to_arduino_type(self.value)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.check_type(scope_chain, diagnostics)

class VariableExpr:
    vname: Token
    ttype: ArduinoType | None
    scope_distance: int

    def __init__(self, token: Token):
        self.vname = token
        self.ttype = None
        self.scope_distance = 0

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.vname.to_string(ntab+2, "vname") + "\n"
        result += f"{" "*(ntab+2)}scope_distance={self.scope_distance}\n"

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result

    def evaluate(self, env: Environment) -> object:
        value = env.get(self.vname.lexeme, self.scope_distance)
        return value

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.vname)

    def check_type(self, scope_chain: ScopeChain, _diagnostics: list[Diagnostic]):
        self.ttype = scope_chain.get_type(self.vname)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.scope_distance = scope_chain.use(self.vname)
        self.check_type(scope_chain, diagnostics)

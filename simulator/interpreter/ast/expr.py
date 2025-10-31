from __future__ import annotations

from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from simulator.interpreter.sema.scope import ScopeChain
    from simulator.interpreter.environment import Environment
    from simulator.interpreter.ast.stmt import Function

from simulator.interpreter.environment import Value
from simulator.interpreter.diagnostic import (ArduinoRuntimeError, 
                                            diagnostic_from_token, Diagnostic)
from simulator.interpreter.lex.token import Token
from simulator.interpreter.sema.types import ArduinoBuiltinType, ArduinoType, coerce_types, token_to_arduino_type, types_compatibility

type Expr = AssignExpr | BinaryExpr | CallExpr | VariableExpr | LiteralExpr

class BinaryOpException(Exception):
    pass

class AssignExpr:
    name: Token
    value: Expr
    ttype: ArduinoType

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

    def evaluate(self, env: Environment):
        value_result = self.value.evaluate(env)
        env.assign(self.name.lexeme, value_result)
        return value_result

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.value.resolve(scope_chain, diagnostics)
        scope_chain.define(self.name)
        self.check_type(scope_chain, diagnostics)

    def check_type(self, scope_chain: ScopeChain, diags: list[Diagnostic]):
        var_type = scope_chain.get_type(self.name)

        if types_compatibility(var_type, self.value.ttype):
            self.ttype = coerce_types(var_type, self.value.ttype)
        else:
            diag = diagnostic_from_token("Type of value assigned is not compatible with variable.", self.name)
            diags.append(diag)
            self.ttype = ArduinoBuiltinType.ERR 


class BinaryExpr:
    lhs: Expr
    op: Token
    rhs: Expr
    ttype: ArduinoType

    op_table = {
        # Arithmetic
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "%": lambda x, y: x % y,
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,

        # Comparison
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
        "<": lambda x, y: x < y,
        "<=": lambda x, y: x <= y,
        ">": lambda x, y: x > y,
        ">=": lambda x, y: x >= y,

        # Bitwise
        "&": lambda x, y: x & y,
        "|": lambda x, y: x | y,
        "^": lambda x, y: x ^ y,
        "<<": lambda x, y: x << y,
        ">>": lambda x, y: x >> y,

        # Logical
        "&&": lambda x, y: bool(x) and bool(y),
        "||": lambda x, y: bool(x) or bool(y),
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
        result += self.lhs.to_string(ntab+2, "lhs")
        result += self.op.to_string(ntab+2, "op") + "\n"
        result += self.rhs.to_string(ntab+2, "rhs")

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return Diagnostic(message, self.op.line, self.op.column, self.op.column)

    def evaluate(self, env: Environment):
        left_value = self.lhs.evaluate(env)
        right_value = self.rhs.evaluate(env)

        if left_value is not None: 
            left_value = left_value.value
        if right_value is not None: 
            right_value = right_value.value

        op_fn = self.op_table[self.op.lexeme]
        try:
            result = op_fn(left_value, right_value)
            return Value(self.ttype, result)
        except TypeError as e:
            raise BinaryOpException(f"{left_value} and {right_value} not compatible") from e

    def check_type(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.lhs.check_type(scope_chain, diagnostics)
        self.rhs.check_type(scope_chain, diagnostics)

        if types_compatibility(self.lhs.ttype, self.rhs.ttype):
            if self.op.is_boolean():
                self.ttype = ArduinoBuiltinType.BOOL
            else:
                self.ttype = coerce_types(self.lhs.ttype, self.rhs.ttype)
                self.ttype = self.lhs.ttype
        else:
            diag = diagnostic_from_token("Types not compatible for this operation.", self.op)
            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR 


    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.lhs.resolve(scope_chain, diagnostics)
        self.rhs.resolve(scope_chain, diagnostics)
        self.check_type(scope_chain, diagnostics)


class CallExpr:
    callee: VariableExpr
    # callee can be the function name (VariableExpr) and a method call on an
    # object (GetExpr). The latter is not implemented yet. 
    arguments: list[Expr]
    ttype: ArduinoType

    def __init__(self, callee: VariableExpr, arguments: list[Expr]):
        self.callee = callee
        self.arguments = arguments
        self.ttype = None

    def evaluate(self, env: Environment):
        fn = self.callee.evaluate(env)

        if not isinstance(fn, Function):
            raise ArduinoRuntimeError("Can only call functions.")

        if len(self.arguments) != fn.arity():
            raise ArduinoRuntimeError(
                f"Expected {fn.arity()} arguments but got {len(self.arguments)}.")

        args = [arg.evaluate(env) for arg in self.arguments]

        return fn.call(args)

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        self.ttype = self.callee.ttype

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.callee.check_type(scope_chain, diagnostics)
        self.check_type(scope_chain, diagnostics)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return self.callee.gen_diagnostic(message)

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.callee.to_string(ntab+2, "callee")
        result += f"{' ' * (ntab + 2)}params=["
        result += ",\n".join([arg.to_string(ntab + 2) for arg in self.arguments])
        result += f"{' ' * (ntab + 2)}],\n"

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result


class LiteralExpr:
    value: Token
    ttype: ArduinoType

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

    def evaluate(self, _env: Environment):
        return Value(self.ttype, self.value.literal)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.value)

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        self.ttype = token_to_arduino_type(self.value)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.check_type(scope_chain, diagnostics)

class VariableExpr:
    vname: Token
    ttype: ArduinoType
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

    def evaluate(self, env: Environment):
        value = env.get(self.vname.lexeme, self.scope_distance)
        return value

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.vname)

    def check_type(self, scope_chain: ScopeChain, _diagnostics: list[Diagnostic]):
        self.ttype = scope_chain.get_type_at(self.vname, self.scope_distance)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.scope_distance = scope_chain.use(self.vname)
        self.check_type(scope_chain, diagnostics)

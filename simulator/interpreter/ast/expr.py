from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from simulator.interpreter.sema.scope import ScopeChain
    from simulator.interpreter.environment import Environment

from simulator.interpreter.ast.stmt import Function
from simulator.interpreter.environment import Value
from simulator.interpreter.diagnostic import (ArduinoRuntimeError, 
                                            diagnostic_from_token, Diagnostic)
from simulator.interpreter.lex.token import Token, TokenType
from simulator.interpreter.sema.types import ArduinoBuiltinType, ArduinoType, coerce_types, token_to_arduino_type, types_compatibility

type Expr = (AssignExpr | BinaryExpr | CallExpr | VariableExpr | LiteralExpr |
    UnaryExpr)

class BinaryOpException(Exception):
    pass

class AssignExpr:
    """
    An assignment expression takes the right-hand operand and assigns it to the
    l-value. 

    The assignment expression evaluates to the l-value after the
    assignment is completed.

    Assignment operators are split into simple assignment '=' and compound
    assignment, like '+='.
    """

    l_value: Expr
    op: Token
    r_value: Expr
    ttype: ArduinoType

    op_table = {
        # Compound arithmetic
        "*=": lambda x, y: x * y,
        "/=": lambda x, y: x / y,
        "%=": lambda x, y: x % y,
        "+=": lambda x, y: x + y,
        "-=": lambda x, y: x - y,

        # Compound bitwise
        "&=": lambda x, y: x & y,
        "|=": lambda x, y: x | y,
        "^=": lambda x, y: x ^ y,

        # Simple
        "=": lambda x, y: y,
    }

    def __init__(self, l_value: Expr, op: Token, r_value: Expr):
        self.l_value = l_value
        self.op = op
        self.r_value = r_value
        self.ttype = None

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.l_value.to_string(ntab+2, "l_value") + "\n"
        result += self.op.to_string(ntab+2, "op") + "\n"
        result += self.r_value.to_string(ntab+2, "r_value") + "\n"

        if self.ttype is not None:
            result += f"{" "*(ntab+2)}ttype={self.ttype}\n"

        result += f"{" "*ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.l_value)

    def evaluate(self, env: Environment) -> Value | None:
        r_value_result = self.r_value.evaluate(env)
        l_value_result = self.l_value.evaluate(env)

        op_fn = self.op_table[self.op.lexeme]
        try:
            l_value = l_value_result.value if l_value_result is not None else None
            r_value = r_value_result.value if r_value_result is not None else None
            result = op_fn(l_value, r_value)
        except TypeError as e:
            raise BinaryOpException(f"{l_value_result} and {r_value_result} not compatible") from e

        # assign name:
        #   var name for VariableExpr
        #   var name and pos for array
        #   field and var name for struct

        if isinstance(self.l_value, VariableExpr): 
            env.assign(self.l_value.vname.lexeme, Value(self.ttype, result))

        return result

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.r_value.resolve(scope_chain, diagnostics)
        self.l_value.resolve(scope_chain, diagnostics)

        if isinstance(self.l_value, VariableExpr): 
            scope_chain.define(self.l_value.vname)

        self.check_type(scope_chain, diagnostics)

    def check_type(self, scope_chain: ScopeChain, diags: list[Diagnostic]):
        var_type = scope_chain.get_type(self.l_value.vname)

        if types_compatibility(var_type, self.l_value.ttype):
            self.ttype = coerce_types(var_type, self.r_value.ttype)
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

    def check_type(self, _scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        if types_compatibility(self.lhs.ttype, self.rhs.ttype):
            if self.op.is_boolean():
                self.ttype = ArduinoBuiltinType.BOOL
            else:
                self.ttype = coerce_types(self.lhs.ttype, self.rhs.ttype)
                self.ttype = self.lhs.ttype
        else:
            diag = diagnostic_from_token(
                    f"Types not compatible for this operation. Left operand: \
{self.lhs.ttype}. Right operand: {self.rhs.ttype}", self.op)

            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR 


    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.lhs.resolve(scope_chain, diagnostics)
        self.rhs.resolve(scope_chain, diagnostics)
        self.check_type(scope_chain, diagnostics)


class UnaryExpr:
    op: Token
    prefix: bool # if false, postfix
    variable: VariableExpr
    ttype: ArduinoType

    def __init__(self, op: Token, prefix: bool, variable: VariableExpr):
        self.op = op
        self.prefix = prefix
        self.variable = variable
        self.ttype = None

    def evaluate(self, env: Environment) -> Value | None:
        var = self.variable.evaluate(env)

        if var is None:
            raise Exception

        new_var = Value(var.value_type, var.value)
        if self.op.token is TokenType.DECREMENT:
            new_var.value = int(var.value) - 1
        else:
            new_var.value = int(var.value) + 1

        env.assign(self.variable.vname.lexeme, new_var)

        if self.prefix:
            return new_var
        else:
            return var

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.variable.resolve(scope_chain, diagnostics)
        if self.variable.ttype not in [ArduinoBuiltinType.INT,
            ArduinoBuiltinType.LONG]:
            diag = diagnostic_from_token(
                "Type of variable must be 'int' or 'long' for decrement or increment.",
                self.variable.vname
            )
            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR
        else:
            self.ttype = self.variable.ttype

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' '*ntab}{name}{self.__class__.__name__}(\n"
        result += self.variable.to_string(ntab+2, "variable")
        result += self.op.to_string(ntab+2, "op")
        result += f"{' ' * (ntab + 2)}position={'prefix' if self.prefix else 'postfix'}"

        if self.ttype is not None:
            result += f"{' '*(ntab+2)}ttype={self.ttype}\n"

        result += f"{' '*ntab})\n"
        return result


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

    def evaluate(self, env: Environment) -> Value | None:
        fn = self.callee.evaluate(env)

        if not isinstance(fn, Function):
            raise ArduinoRuntimeError("Can only call functions.")

        if len(self.arguments) != fn.arity():
            raise ArduinoRuntimeError(
                f"Expected {fn.arity()} arguments but got {len(self.arguments)}.")

        fn_args = [fn_arg.evaluate(env) for fn_arg in self.arguments]

        return fn.call(fn_args)

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        self.ttype = self.callee.ttype

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.callee.check_type(scope_chain, diagnostics)
        for call_arg in self.arguments:
            call_arg.resolve(scope_chain, diagnostics)
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

    def evaluate(self, _env: Environment) -> Value:
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

    def evaluate(self, env: Environment) -> Value | None:
        value = env.get(self.vname.lexeme, self.scope_distance)
        return value

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.vname)

    def check_type(self, scope_chain: ScopeChain, _diagnostics: list[Diagnostic]):
        self.ttype = scope_chain.get_type_at(self.vname, self.scope_distance)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.scope_distance = scope_chain.use(self.vname)
        self.check_type(scope_chain, diagnostics)

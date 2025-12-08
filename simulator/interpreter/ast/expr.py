from __future__ import annotations

from typing import TYPE_CHECKING, override

if TYPE_CHECKING:
    from simulator.interpreter.sema.scope import ScopeChain
    from simulator.interpreter.environment import Environment

from simulator.interpreter.runtime.classes import (
    ArduinoClass,
    ArduinoInstance,
)
from simulator.interpreter.environment import Value
from simulator.interpreter.diagnostic import (
    ArduinoRuntimeError,
    diagnostic_from_token,
    Diagnostic,
)
from simulator.interpreter.lex.token import Token, TokenType
from simulator.interpreter.sema.types import (
    ArduinoArray,
    ArduinoObjType,
    ArduinoBuiltinType,
    ArduinoType,
    coerce_types,
    token_to_arduino_type,
    types_compatibility,
)

type Expr = (
    ArrayInitExpr
    | AssignExpr
    | BinaryExpr
    | CallExpr
    | CastExpr
    | GetExpr
    | VariableExpr
    | LiteralExpr
    | UnaryExpr
    | ArrayRefExpr
)


class BinaryOpException(Exception):
    pass


class ArrayInitExpr:
    init_list: list[Expr]
    ttype: ArduinoType

    def __init__(self, init_list: list[Expr]):
        self.init_list = init_list
        self.ttype = None

    @override
    def __repr__(self) -> str:
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += ",\n".join([init.to_string(ntab + 2) for init in self.init_list])

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate(self, environment: Environment) -> Value:
        value_list = [expr.evaluate(environment) for expr in self.init_list]

        return Value(self.ttype, value_list)

    def evaluate_l(self, env: Environment):
        pass

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        ttypes: list[ArduinoType] = []

        for expr in self.init_list:
            expr.resolve(scope_chain, diagnostics)
            ttypes.append(expr.ttype)

        if len(set(ttypes)) == 1:
            inner_type = ttypes[0]
            self.ttype = ArduinoArray(inner_type)
        else:
            self.init_list.gen_diagnostic("Array initializer must be of a single type.")


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

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.l_value.to_string(ntab + 2, "l_value") + "\n"
        result += self.op.to_string(ntab + 2, "op") + "\n"
        result += self.r_value.to_string(ntab + 2, "r_value") + "\n"

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.l_value)

    def evaluate(self, env: Environment) -> Value | None:
        # An lvalue expr evaluates to a function that given a value x, will assign
        # that x value to the resulting expr.
        #
        # For a VariableExpr, this is a function that sets value x to the
        # identifier in the corresponding Environment.
        # For a simple ArrayRefExpr, like a[0], this is a function that sets value x to the array
        # slot inside the variable value in the corresponding Environment.

        r_value_result = self.r_value.evaluate(env)
        l_value_result = self.l_value.evaluate(env)
        l_value_assign_fn = self.l_value.evaluate_l(env)
        assert l_value_assign_fn is not None

        op_fn = self.op_table[self.op.lexeme]
        try:
            l_value = l_value_result.value if l_value_result is not None else None
            r_value = r_value_result.value if r_value_result is not None else None
            result = op_fn(l_value, r_value)
        except TypeError as e:
            raise BinaryOpException(
                f"{l_value_result} and {r_value_result} not compatible"
            ) from e

        return l_value_assign_fn(result)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.r_value.resolve(scope_chain, diagnostics)
        self.l_value.resolve(scope_chain, diagnostics)

        if isinstance(self.l_value, VariableExpr):
            scope_chain.define(self.l_value.vname)

        self.check_type(scope_chain, diagnostics)

    def evaluate_l(self, env: Environment):
        return self.evaluate

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.resolve(scope_chain, diagnostics)

    def check_type(self, _scope_chain: ScopeChain, diags: list[Diagnostic]):
        if types_compatibility(self.l_value.ttype, self.r_value.ttype):
            self.ttype = coerce_types(self.l_value.ttype, self.r_value.ttype)
        else:
            diag = diagnostic_from_token(
                "Type of value assigned is not compatible with variable.", self.op
            )
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

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.lhs.to_string(ntab + 2, "lhs")
        result += self.op.to_string(ntab + 2, "op") + "\n"
        result += self.rhs.to_string(ntab + 2, "rhs")

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return Diagnostic(message, self.op.line, self.op.column, self.op.column)

    def evaluate(self, env: Environment):
        left = self.lhs.evaluate(env)
        right = self.rhs.evaluate(env)

        if left is not None:
            left_value = left.value
        if right is not None:
            right_value = right.value

        op_fn = self.op_table[self.op.lexeme]
        try:
            result = op_fn(left_value, right_value)
            val = Value(self.ttype, result)
            return val
        except TypeError as e:
            raise BinaryOpException(
                f"{left_value} and {right_value} not compatible"
            ) from e

    def check_type(self, _scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        if types_compatibility(self.lhs.ttype, self.rhs.ttype):
            if self.op.is_boolean():
                self.ttype = ArduinoBuiltinType.BOOL
            else:
                self.ttype = coerce_types(self.lhs.ttype, self.rhs.ttype)
        else:
            diag = diagnostic_from_token(
                f"Types not compatible for this operation. Left operand: \
{self.lhs.ttype}. Right operand: {self.rhs.ttype}",
                self.op,
            )

            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.lhs.resolve(scope_chain, diagnostics)
        self.rhs.resolve(scope_chain, diagnostics)
        self.check_type(scope_chain, diagnostics)

    def evaluate_l(self, env: Environment):
        pass

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        pass


class UnaryExpr:
    op: Token
    prefix: bool  # if false, postfix
    operand: Expr  # the operand must be an l-value
    ttype: ArduinoType

    op_table = {
        # Arithmetic
        "++": lambda x: int(x) + 1,
        "--": lambda x: int(x) - 1,
        # Logical
        "!": lambda x: not x,
        # Bitwise
        "~": lambda x: ~int(x),
    }

    def __init__(self, op: Token, prefix: bool, operand: Expr):
        self.op = op
        self.prefix = prefix
        self.operand = operand
        self.ttype = None

    @override
    def __repr__(self):
        return self.to_string()

    def evaluate(self, env: Environment) -> Value | None:
        var = self.operand.evaluate(env)
        operand_assign_fn = self.operand.evaluate_l(env)

        if var is None:
            raise Exception

        op_fn = self.op_table[self.op.lexeme]

        new_var = operand_assign_fn(op_fn(var.value))

        if self.prefix:
            return new_var
        else:
            return var

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.operand.resolve(scope_chain, diagnostics)
        if (
            self.op.token is TokenType.LOGICAL_NOT
            and self.operand.ttype is not ArduinoBuiltinType.BOOL
        ):
            diag = diagnostic_from_token(
                "Type of expr must be 'bool' for logical not.", self.op
            )
            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR
        elif self.op.token in [
            TokenType.INCREMENT,
            TokenType.DECREMENT,
            TokenType.BITWISE_NOT,
        ] and self.operand.ttype not in [
            ArduinoBuiltinType.INT,
            ArduinoBuiltinType.LONG,
        ]:
            diag = diagnostic_from_token(
                f"Type of expr must be 'int' or 'long' for {self.op.token}.",
                self.op,
            )
            diagnostics.append(diag)
            self.ttype = ArduinoBuiltinType.ERR
        else:
            self.ttype = self.operand.ttype

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.operand.to_string(ntab + 2, "expr")
        result += self.op.to_string(ntab + 2, "op")
        result += f"{' ' * (ntab + 2)}position={'prefix' if self.prefix else 'postfix'}"

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate_l(self, env: Environment):
        pass

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        pass


class ArrayRefExpr:
    primary: Expr
    index: Expr
    ttype: ArduinoType

    def __init__(self, primary: Expr, index: Expr):
        self.primary = primary
        self.index = index
        self.ttype = None

    @override
    def __repr__(self) -> str:
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.primary.to_string(ntab + 2, "primary")
        result += self.index.to_string(ntab + 2, "index")

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate(self, environment: Environment) -> Value:
        array_var = self.primary.evaluate(environment)
        index_val = self.index.evaluate(environment)

        assert array_var is not None
        assert isinstance(array_var.value, list)
        assert index_val is not None

        try:
            result = array_var.value[index_val.value]
        except IndexError:
            self.gen_diagnostic("Index out of array bounds.")

        return result

    def evaluate_l(self, env: Environment):
        def set_value(x: object):
            array_var = self.primary.evaluate(env)

            value = Value(self.ttype, x)
            array_var.value.__setitem__(self.index.evaluate(env).value, value)
            return value

        return set_value

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        array_type = self.primary.ttype

        while isinstance(array_type, ArduinoArray):
            array_type = array_type.ttype

        self.ttype = array_type

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.primary.resolve(scope_chain, diagnostics)
        self.index.resolve(scope_chain, diagnostics)
        if self.index.ttype not in [
            ArduinoBuiltinType.INT,
            ArduinoBuiltinType.LONG,
            ArduinoBuiltinType.SHORT,
        ]:
            diag = self.gen_diagnostic("Array reference expr must be of type integral.")
            diagnostics.append(diag)
        self.check_type(scope_chain, diagnostics)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return self.index.gen_diagnostic(message)


class GetExpr:
    obj: Expr
    name: Token
    ttype: ArduinoType

    def __init__(self, obj: Expr, name: Token) -> None:
        self.obj = obj
        self.name = name
        self.ttype = None

    @override
    def __repr__(self) -> str:
        return self.to_string()

    def evaluate(self, env: Environment) -> Value | None:
        obj = self.obj.evaluate(env)
        if obj and isinstance(obj.value, ArduinoInstance):
            method = obj.value.get(self.name)
        elif obj and isinstance(obj.value, ArduinoClass):
            method = obj.value.find_method(self.name.lexeme)
        else:
            raise ArduinoRuntimeError(f"Expected object or class name.")
        return method

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.obj.resolve(scope_chain, diagnostics)
        self.ttype = self.obj.ttype

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.obj.to_string(ntab + 2, "obj")
        result += self.name.to_string(ntab + 2, "name")

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate_l(self, env: Environment):
        pass

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        pass


class CallExpr:
    callee: Expr
    # callee can be the function name (VariableExpr) and a method call on an
    # object (GetExpr). The latter is not implemented yet.
    arguments: list[Expr]
    ttype: ArduinoType

    def __init__(self, callee: Expr, arguments: list[Expr]):
        self.callee = callee
        self.arguments = arguments
        self.ttype = None

    @override
    def __repr__(self) -> str:
        return self.to_string()

    def evaluate(self, env: Environment) -> Value | None:
        callee = self.callee.evaluate(env)

        if len(self.arguments) not in callee.value.arity():
            raise ArduinoRuntimeError(
                f"Error calling {callee.value}. Expected {callee.value.arity()} arguments but got {len(self.arguments)}."
            )

        fn_args = [fn_arg.evaluate(env) for fn_arg in self.arguments]

        val = callee.value.call(fn_args, callee.value_type)
        if not isinstance(val, Value):
            val = Value(self.ttype, val)
        return val

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        self.ttype = self.callee.ttype

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.callee.resolve(scope_chain, diagnostics)
        for call_arg in self.arguments:
            call_arg.resolve(scope_chain, diagnostics)
        self.check_type(scope_chain, diagnostics)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return self.callee.gen_diagnostic(message)

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.callee.to_string(ntab + 2, "callee")
        result += f"{' ' * (ntab + 2)}params=["
        result += ",\n".join([arg.to_string(ntab + 2) for arg in self.arguments])
        result += f"{' ' * (ntab + 2)}],\n"

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate_l(self, env: Environment):
        pass

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        pass


class CastExpr:
    cast_type: Token
    value: Expr
    ttype: ArduinoType

    def __init__(self, cast_type: Token, value: Expr):
        self.cast_type = cast_type
        self.value = value
        self.ttype = None

    @override
    def __repr__(self) -> str:
        return self.to_string()

    def evaluate(self, env: Environment) -> Value | None:
        value = self.value.evaluate(env)
        if value is not None:
            value.coerce(self.ttype)
        return value

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.value.resolve(scope_chain, diagnostics)
        self.ttype = token_to_arduino_type(self.cast_type)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return self.value.gen_diagnostic(message)

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.cast_type.to_string(ntab + 2, "cast_type")
        result += self.value.to_string(ntab + 2, "value")

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate_l(self, env: Environment):
        pass

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        pass


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

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.value.to_string(ntab + 2, "value") + "\n"

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate(self, _env: Environment) -> Value:
        if self.ttype == ArduinoObjType("String"):
            string_value = "".join(
                map(lambda tok: chr(tok.literal), self.value.literal)
            )
            return Value(self.ttype, string_value)

        return Value(self.ttype, self.value.literal)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.value)

    def check_type(self, _scope_chain: ScopeChain, _diags: list[Diagnostic]):
        self.ttype = token_to_arduino_type(self.value)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.check_type(scope_chain, diagnostics)

    def evaluate_l(self, env: Environment):
        pass

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        pass


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

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.vname.to_string(ntab + 2, "vname") + "\n"
        result += f"{' ' * (ntab + 2)}scope_distance={self.scope_distance}\n"

        if self.ttype is not None:
            result += f"{' ' * (ntab + 2)}ttype={self.ttype}\n"

        result += f"{' ' * ntab})\n"
        return result

    def evaluate(self, env: Environment) -> Value | None:
        value = env.get(self.vname.lexeme, self.scope_distance)
        return value

    def evaluate_l(self, env: Environment):
        def set_value(x: object):
            val = Value(self.ttype, x)
            val.coerce(self.ttype)
            env.assign(self.vname.lexeme, val)
            return val

        return set_value

    def resolve_l(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        scope_chain.define(self.vname)
        self.check_type(scope_chain, diagnostics)

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.vname)

    def check_type(self, scope_chain: ScopeChain, _diagnostics: list[Diagnostic]):
        self.ttype = scope_chain.get_type_at(self.vname, self.scope_distance)

    def resolve(self, scope_chain: ScopeChain, diagnostics: list[Diagnostic]):
        self.scope_distance = scope_chain.use(self.vname)
        self.check_type(scope_chain, diagnostics)

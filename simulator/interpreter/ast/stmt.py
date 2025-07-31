from dataclasses import dataclass
from typing import override

import simulator.interpreter.sema.scope as scope
import simulator.interpreter.ast.expr as expr
from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.lex.token import Token
from simulator.interpreter.sema.types import (
    ArduinoBuiltinType,
    ArduinoType,
    coerce_types,
    token_to_arduino_type,
    types_compatibility,
)

type Stmt = BlockStmt | ExpressionStmt | FunctionStmt | ReturnStmt | VariableStmt


@dataclass
class BlockStmt:
    stmts: list[Stmt]
    ttype: ArduinoType

    def execute(self, env: Environment):
        block_env = Environment(enclosing=env)

        for stmt in self.stmts:
            stmt.execute(block_env)

        del block_env

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        scope_chain.begin_scope()

        for stmt in self.stmts:
            stmt.resolve(scope_chain, diagnostics)

        last_stmt = self.stmts[-1]

        if isinstance(last_stmt, ReturnStmt):
            self.ttype = last_stmt.ttype
        else:
            self.ttype = ArduinoBuiltinType.VOID

        scope_chain.end_scope()

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        for stmt in self.stmts:
            result += stmt.to_string(ntab + 2) + "\n"

        result += f"{' ' * (ntab + 2)}stmts=["
        result += ",\n".join([stmt.to_string(ntab + 4) for stmt in self.stmts])
        result += f"{' ' * (ntab + 2)}],\n"

        result += f"{' ' * ntab})\n"
        return result


@dataclass
class ExpressionStmt:
    expr: expr.Expr

    def execute(self, env: Environment):
        self.expr.evaluate(env)

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        self.expr.resolve(scope_chain, diagnostics)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.expr.to_string(ntab + 2, "expr") + "\n"
        result += f"{' ' * ntab})\n"
        return result


@dataclass
class ReturnStmt:
    expr: expr.Expr
    ttype: ArduinoType

    def execute(self, env: Environment):
        value = self.expr.evaluate(env)
        raise ReturnException(value)

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        self.expr.resolve(scope_chain, diagnostics)
        self.ttype = self.expr.ttype

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += self.expr.to_string(ntab + 2, "expr")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})\n"
        return result


@dataclass
class VariableStmt:
    var_type: Token
    name: Token
    initializer: expr.Expr | None
    ttype: ArduinoType

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.var_type.to_string(ntab + 2, "var_type")
        result += ",\n" + self.name.to_string(ntab + 2, "name")

        if self.initializer is not None:
            result += ",\n" + self.initializer.to_string(ntab + 2, "initializer")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def execute(self, environment: Environment):
        init_value = None
        if self.initializer is not None and self.initializer.ttype is not None:
            init_value = self.initializer.evaluate(environment)
            if (
                init_value
                and isinstance(init_value, Value)
                and init_value.value_type is not self.ttype
            ):
                init_value.coerce(self.ttype)

            environment.define(self.name.lexeme, init_value)
        else:
            environment.define(self.name.lexeme, None)

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        if self.initializer:
            self.initializer.resolve(scope_chain, diagnostics)

        self.ttype = self._compute_type(scope_chain, diagnostics)
        scope_chain.declare(self.name, self.ttype)

        if self.initializer:
            scope_chain.define(self.name)

    def _compute_type(
        self, _scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]
    ) -> ArduinoType:
        var_arduino_type = token_to_arduino_type(self.var_type)

        if not self.initializer:
            return var_arduino_type

        if self.initializer and types_compatibility(
            var_arduino_type, self.initializer.ttype
        ):
            return var_arduino_type

        diag = self.gen_diagnostic(
            "Initializer expression has incompatible types. Initializer: " +
                f"{self.initializer.ttype}. Variable: {var_arduino_type}")
        diagnostics.append(diag)
        return ArduinoBuiltinType.ERR


@dataclass
class FunctionStmt:
    name: Token
    params: list[VariableStmt]
    body: list[Stmt]
    return_type: Token
    ttype: ArduinoType

    def execute(self, env: Environment):
        fn = Function(self.params, self.body, env)
        env.define(self.name.lexeme, fn)

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        scope_chain.begin_scope()

        for param in self.params:
            param.resolve(scope_chain, diagnostics)
        for stmt in self.body:
            stmt.resolve(scope_chain, diagnostics)

        scope_chain.end_scope()

        arduino_return_type = token_to_arduino_type(self.return_type)

        last_stmt = self.body[-1]

        if isinstance(last_stmt, ReturnStmt):
            last_stmt_type = last_stmt.ttype
        else:
            last_stmt_type = ArduinoBuiltinType.VOID

        if types_compatibility(arduino_return_type, last_stmt_type):
            self.ttype = coerce_types(arduino_return_type, last_stmt_type)
            scope_chain.declare(self.name, self.ttype)
        else:
            diag = diagnostic_from_token(
                "Function type and actual return type are incompatible",
                self.return_type,
            )
            diagnostics.append(diag)

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{' ' * ntab}{name}{self.__class__.__name__}(\n"
        result += "\n" + self.name.to_string(ntab + 2, "name")

        result += f"{' ' * (ntab + 2)}params=["
        result += ",\n".join([param.to_string(ntab + 4) for param in self.params])
        result += f"{' ' * (ntab + 2)}],\n"

        result += self.body.to_string(ntab + 2, "body")
        result += self.return_type.to_string(ntab + 2, "return_type")

        if self.ttype is not None:
            result += ",\n" + f"{' ' * (ntab + 2)}ttype={self.ttype}"

        result += f"{' ' * ntab})\n"
        return result


class ReturnException(Exception):
    value: object

    def __init__(self, ret_value: object):
        super().__init__()
        self.value = ret_value


@dataclass
class Function:
    """
    Function in the Arduino language.
    """

    params: list[VariableStmt]
    body: list[Stmt]
    closure: Environment

    def arity(self) -> int:
        "Returns the function's number of parameters"

        return len(self.params)

    def call(self, arguments: list[object]) -> object:
        "Call the function and return."

        fn_env = Environment(self.closure)

        for param, arg in zip(self.params, arguments):
            fn_env.define(param.name.lexeme, arg)

        try:
            for stmt in self.body:
                stmt.execute(fn_env)
        except ReturnException as ret:
            return ret.value

        return None

from dataclasses import dataclass
from typing import override

import simulator.interpreter.scope as scope
import simulator.interpreter.expr as expr
from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.token import Token
from simulator.interpreter.types import ArduinoBuiltinType, ArduinoType, coerce_types, token_to_arduino_type, types_compatibility

type Stmt = BlockStmt | ExpressionStmt | VariableStmt

@dataclass
class BlockStmt:
    stmts: list[Stmt]

    def execute(self, env: Environment):
        block_env = Environment(enclosing=env)

        for stmt in self.stmts:
            stmt.execute(block_env)

        del block_env

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        scope_chain.begin_scope()

        for stmt in self.stmts:
            stmt.resolve(scope_chain, diagnostics)

        scope_chain.end_scope()

    @override
    def __repr__(self):
        return self.to_string()

    def to_string(self, ntab: int = 0, name: str = "") -> str:
        if name != "":
            name += "="

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        for stmt in self.stmts:
            result += stmt.to_string(ntab+2) + "\n"

        result += f"{" "*ntab})\n"
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

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}(\n"
        result += self.expr.to_string(ntab+2, "expr") + "\n"
        result += f"{" "*ntab})\n"
        return result

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

        result: str = f"{" "*ntab}{name}{self.__class__.__name__}("
        result += "\n" + self.var_type.to_string(ntab+2, "var_type")
        result += ",\n" + self.name.to_string(ntab+2, "name")

        if self.initializer is not None:
            result += ",\n" + self.initializer.to_string(ntab+2, "initializer")

        if self.ttype is not None:
            result += ",\n" + f"{" "*(ntab+2)}ttype={self.ttype}"

        result += f"{" "*ntab})\n"
        return result

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def execute(self, environment: Environment):
        init_value = None
        if self.initializer is not None and self.initializer.ttype is not None:
            init_value = self.initializer.evaluate(environment)
            if init_value and init_value.value_type is not self.ttype:
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

    def _compute_type(self, _scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]) -> ArduinoType:
        var_arduino_type = token_to_arduino_type(self.var_type)

        if (self.initializer and
            types_compatibility(var_arduino_type, self.initializer.ttype)):
            return var_arduino_type

        diag = self.gen_diagnostic("Initializer expression has incompatible types.")
        diagnostics.append(diag)
        return ArduinoBuiltinType.ERR


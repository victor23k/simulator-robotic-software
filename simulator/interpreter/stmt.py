from dataclasses import dataclass

import simulator.interpreter.scope as scope
import simulator.interpreter.expr as expr
from simulator.interpreter.diagnostic import Diagnostic, diagnostic_from_token
from simulator.interpreter.environment import Environment, Value
from simulator.interpreter.token import Token
from simulator.interpreter.types import ArduinoBuiltinType, ArduinoType, token_to_arduino_type

type Stmt = ExpressionStmt | VariableStmt

@dataclass
class ExpressionStmt:
    expr: expr.Expr

    def execute(self, env: Environment):
        self.expr.evaluate(env)

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        self.expr.resolve(scope_chain, diagnostics)

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
    ttype: ArduinoType | None

    def gen_diagnostic(self, message: str) -> Diagnostic:
        return diagnostic_from_token(message, self.name)

    def execute(self, environment: Environment):
        init_value = None
        if self.initializer is not None and self.initializer.ttype is not None:
            init_value = self.initializer.evaluate(environment)
            value = Value(self.initializer.ttype, init_value)
            environment.define(self.name.lexeme, value)
        else:
            environment.define(self.name.lexeme, None)

    def resolve(self, scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]):
        if self.initializer:
            self.initializer.resolve(scope_chain, diagnostics)

        ttype = self._compute_type(scope_chain, diagnostics)
        scope_chain.declare(self.name, ttype)

        if self.initializer:
            scope_chain.define(self.name)

    def _compute_type(self, _scope_chain: scope.ScopeChain, diagnostics: list[Diagnostic]) -> ArduinoType:
        var_arduino_type = token_to_arduino_type(self.var_type)
        if self.initializer and self.initializer.ttype is var_arduino_type:
            return var_arduino_type

        diag = self.gen_diagnostic("Initializer expression has incompatible types.")
        diagnostics.append(diag)
        return ArduinoBuiltinType.ERR

